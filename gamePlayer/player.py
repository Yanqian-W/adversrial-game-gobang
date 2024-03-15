import random


def random_player(game, state):
    if state.to_move == 'O':
        color = "white"
    else:
        color = "black"
    (x, y) = random.choice(list(game.actions(state)))
    game.visualize.draw_piece((x, y), color)
    return (x, y)


def human_player(game, state):
    """Make a move by reading input."""
    print(state)
    print('Legal moves are', game.actions(state))
    move = None
    while move not in game.actions(state):
        move = eval(input('Your move? '))
    # vis.draw_piece(move,"black")
    print(move)
    return move


def human_mouse_player(game, state):
    """Make a move by reading input."""
    move = None
    while move not in game.actions(state):
        move = game.visualize.get_input()
    return move


def player(search_algorithm):
    """A game player who uses the specified search algorithm"""
    return lambda game, state: search_algorithm(game, state)[1]