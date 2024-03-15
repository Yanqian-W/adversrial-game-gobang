from gameBoard.board import Board
from gameBoard.visualize import Visualize


class goBang():
    """
    Play goBang on an `height` by `width` board, needing `k` in a row (column or diagonal) to win.
    'X' plays first against 'O'.
    """

    def __init__(self, height=16, width=16, k=5):
        self.height = height
        self.width = width
        self.k = k
        self.squares = {(x, y) for x in range(width) for y in range(height)}
        # initially, the utility function is 0
        self.board = Board(height=height, width=width, to_move='X', utility=0)

        # visualize the game
        self.visualize = Visualize()
        self.visualize.draw_board()

    def utility(self, board, player):
        """
        Return the terminal state utility value corresponding to different players;
        pow(1000,6) for win, -pow(1000,6) for loss, 0 otherwise.
        """
        return board.utility if player == 'X' else -board.utility

    def actions(self, board):
        """Legal moves are any square not yet taken."""
        return self.squares - set(board)

    def result(self, board, square):
        """Place a marker for current player on square."""
        player = board.to_move
        board = board.new({square: player}, to_move=('O' if player == 'X' else 'X'))
        win = k_in_row(board, player, square, self.k)
        # 0 for not win, pow(1000,6) for win, -pow(1000,6) for lose
        board.utility = (0 if not win else + pow(1000, self.k + 1) if player == 'X' else -pow(1000, self.k + 1))
        return board

    def is_terminal(self, board):
        """A board is a terminal state if it is won or there are no empty squares."""
        return board.utility != 0 or len(self.squares) == len(board)

    def has_neighbour(self, square, place):
        """
        Is this square has neighbour?
        agent will not place a piece if it has no neighbour pieces on the board
        this method can reduce the size of the problem by not examing pieces with no neighbours
        """
        x, y = square
        place_temp = place.copy()

        # allow the first move to be placed as the neighbor of the centerpiece
        if len(place_temp) == self.height * self.width:  # if the board is empty
            place_temp.remove((round(self.height / 2), round(self.width / 2)))

        for i in range(-1, 2):
            for j in range(-1, 2):
                # identify the squares have neighbour pieces
                if not ((x + i, y + j) in place_temp) and ((x + i, y + j) in self.squares):
                    return True
        return False

    def board_status(self, board, player, k):
        """The method checking if player has k pieces in a line.
         Along the line, count the number of one-side dead, two-side dead and life ending squares
         life => no piece on both ending sides of the line;
         one_dead => no piece on one ending side of the line;
         both_dead => both ending sides occupied
         """
        life = 0
        one_dead = 0
        both_dead = 0

        directions = [(-1, 0), (1, 0), (-1, 1), (1, -1), (0, 1), (0, -1), (1, 1), (-1, -1)]
        for row in range(self.width):
            for col in range(self.height):
                # If this is not the current player, skip it
                if board[row, col] != player:
                    continue
                j = 0
                while j < len(directions):
                    a = 0  # a represents two different directions
                    count = 1  # the number of pieces for current player in this line
                    # record[0] and record[1] respectively indicate whether there is obstruction at both ends
                    record = [0, 0]
                    # Cycle twice to determine two opposite directions
                    while a <= 1:
                        x, y = row, col
                        for i in range(4):
                            # Search four squares in this direction
                            x += directions[j][0]
                            y += directions[j][1]
                            # Call the internal __missing__ method of the Board class
                            if board[x, y] == '#':
                                # Beyond the boundary
                                record[a] = 1
                                break
                            if board[x, y] == player:
                                count += 1
                            elif board[x, y] == ('X' if player == 'O' else 'O'):
                                # The opponent's piece appears
                                record[a] = 1
                                break
                            else:
                                # Blank space appears
                                record[a] = 0
                                break
                        a += 1
                        j += 1

                    if count == k:
                        if record[0] == record[1] == 0:
                            # There are k consecutive pieces and neither side is blocked
                            life += 1
                        elif record[0] == record[1] == 1:
                            # There are k consecutive pieces and both sides are blocked
                            both_dead += 1
                        else:
                            # There are consecutive k pieces and only one side is blocked
                            one_dead += 1

        # Each method is recalculated k times
        life = int(life / k)
        one_dead = int(one_dead / k)
        both_dead = int(both_dead / k)

        return life, one_dead, both_dead

    def get_heuristic_score(self, board, player):
        """
        Estimate non-terminal board's utility, given the current player.
        Taking the 'board status' into consideration, estimation utility value as a score evaluating
        the possibility of the player winning the game.
        Return the score.
        """
        score = 0

        # five pieces
        lifeFive, one_deadFive, both_deadFive = self.board_status(board, player, 5)
        if lifeFive > 0 or one_deadFive > 0 or both_deadFive > 0:
            return 1000000

        # four pieces
        lifeFour, one_deadFour, both_deadFour = self.board_status(board, player, 4)
        if lifeFour > 0 or one_deadFour > 1:
            return 900000
        elif one_deadFour == 1:
            score += 10000
        if both_deadFour > 0:
            score += 100 * both_deadFour

        # three pieces
        lifeThree, one_deadThree, both_deadThree = self.board_status(board, player, 3)
        if lifeThree > 1:
            return 800000
        elif lifeThree == 1:
            score += 10000
        if one_deadThree > 0:
            score += 10 * one_deadThree
        if both_deadThree > 0:
            score += 0

        # two pieces
        lifeTwo, one_deadTwo, both_deadTwo = self.board_status(board, player, 2)
        if lifeTwo > 0:
            score += 100 * lifeTwo
        if one_deadTwo > 0:
            score += 10 * one_deadTwo
        if both_deadTwo > 0:
            score += 0

        return score

    def board_score(self, board, square):
        """Utilize the heuristic method to estimate the utility of the game board
        that applying potential move specified by `square`.
        The new board's utility estimation takes both players into consideration. """

        player = board.to_move

        # update the board by performing the move specified by square
        board = board.new({square: player}, to_move=('O' if player == 'X' else 'X'))
        # calculate the board estimated utility taking both
        adjust_weight = 30  # you can try a different adjust_weight to see what will happen
        board_score = self.get_heuristic_score(board, player) - adjust_weight * self.get_heuristic_score(board, (
            'O' if player == 'X' else 'X'))
        return board_score

    def display(self):
        print(self.board)


def k_in_row(board, player, square, k):
    """True if player has k pieces in a line through square."""

    def in_row(x, y, dx, dy): return 0 if board[x, y] != player else 1 + in_row(x + dx, y + dy, dx, dy)

    return any(in_row(*square, dx, dy) + in_row(*square, -dx, -dy) - 1 >= k
               for (dx, dy) in ((0, 1), (1, 0), (1, 1), (1, -1)))
