import sys
import pygame
from gameStrategy.goBang import goBang
from gameBoard.visualize import Visualize
from gameBoard.board import Board
from gamePlayer.player import player, human_mouse_player
from gameStrategy.SearchAlgorithm import limited_alphabeta_search


def play_game(game, strategies: dict, verbose=False):
    """
    Play a turn-taking game. `strategies` is a {player_name: function} dict,
    where function(state, game) is used to get the player's move.
    """
    state = game.initial
    visualize = game.visualize

    while not game.is_terminal(state):
        player = state.to_move
        move = strategies[player](game, state)
        state = game.result(state, move)
        visualize.draw_piece(move, visualize.BLACK if player == 'X' else visualize.WHITE)
        print('Player', player, ':', move)
        if verbose:
            print(state)
    print('Game over: utility', game.utility(state, 'X'), 'for X')

    # exit or restart the GUI
    again = visualize.draw_end_screen(1 if game.utility(state, 'X') > 0 else 2 if game.utility(state, 'X') < 0 else 0)
    if again == 0:
        main()
    else:
        pygame.quit()
        sys.exit()

    return state


def main():
    # play_game(goBang(), dict(X=human_mouse_player, O=human_mouse_player), verbose=False).utility
    play_game(goBang().display(), dict(X=human_mouse_player, O=player(limited_alphabeta_search)), verbose=False)
    # play_game(goBang(), dict(X=player(limited_alphabeta_search),
    #   O=player(limited_alphabeta_search)), verbose=False).utility
    # play_game(goBang(), dict(X=player(limited_alphabeta_search),
    #   O=player(limited_minimax_search)), verbose=False).utility

    if __name__ == '__main__':
        main()
