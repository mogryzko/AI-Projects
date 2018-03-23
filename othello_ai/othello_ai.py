#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to
complete and submit.

@author: Max Ogryzko mvo2102
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

start_time = time.time()
board_dict = {}





def mySort(board, actions, color):
    """
    Takes in the current board and a list of possible moves, returns that list
    organized by their utility (largest -> smallest)
    """
    util = []
    for i in range(len(actions)):
        utility = compute_utility(play_move(board, color, actions[i][0], actions[i][1]), color)
        util.append((utility, actions[i]))
    util.sort(reverse=True)
    return_list = []
    for j in range(len(util)):
        return_list.append(util[j][1])
    return return_list


def compute_utility(board, color):
    if (color == 1):
        return (get_score(board)[0] - get_score(board)[1])
    else:
        return (get_score(board)[1] - get_score(board)[0])

    return 0


############ MINIMAX ###############################

def minimax_min_node(board, color):
    if color == 1:
        oppositecolor = 2
    else:
        oppositecolor = 1

    if not (get_possible_moves(board, color)):
        return compute_utility(board, oppositecolor)
    elif (board in board_dict):
        return board_dict[board]
    else:
        actions = get_possible_moves(board, color)
        min = float('inf')
        for i in range(0, len(actions)):
            temp = minimax_max_node(play_move(board, color, actions[i][0], actions[i][1]), oppositecolor)
            if min > temp:
                min = temp
        board_dict[board] = min
        return min


def minimax_max_node(board, color):
    if color == 1:
        oppositecolor = 2
    else:
        oppositecolor = 1

    if not (get_possible_moves(board, color)):
        return compute_utility(board, color)
    elif (board in board_dict):
        return board_dict[board]
    else:
        actions = get_possible_moves(board, color)
        max = float('-inf')
        for i in range(0, len(actions)):
            temp = minimax_min_node(play_move(board, color, actions[i][0], actions[i][1]), oppositecolor)
            if max < temp:
                max = temp
        board_dict[board] = max
        return max


def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    if color == 1:
        oppositecolor = 2
    else:
        oppositecolor = 1
    actions = get_possible_moves(board, color)
    max = float('-inf')
    finalmax = actions[0]
    for i in range(0, len(actions)):
        if (play_move(board, color, actions[i][0], actions[i][1]) in board_dict):
            temp = board_dict[play_move(board, color, actions[i][0], actions[i][1])]
        else:
            temp = minimax_min_node(play_move(board, color, actions[i][0], actions[i][1]), oppositecolor)
        if max < temp:
            max = temp
            finalmax = actions[i]
    return finalmax


############ ALPHA-BETA PRUNING #####################

# alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta):
    if color == 1:
        oppositecolor = 2
    else:
        oppositecolor = 1

    if (time.time() - start_time) > 9.9:
        return compute_utility(board, oppositecolor)
    elif (board in board_dict):
        return board_dict[board]
    else:
        value = float('inf')
        pre_actions = get_possible_moves(board, color)
        actions = mySort(board, pre_actions, oppositecolor)
        for i in range(0, len(actions)):
            value = min(value,
                        alphabeta_max_node(play_move(board, color, actions[i][0], actions[i][1]), oppositecolor, alpha,
                                           beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        board_dict[board] = value
        return value


# alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta):
    if color == 1:
        oppositecolor = 2
    else:
        oppositecolor = 1

    if (time.time() - start_time) > 9.9:
        return compute_utility(board, color)
    elif (board in board_dict):
        return board_dict[board]
    else:
        value = float('-inf')
        pre_actions = get_possible_moves(board, color)
        actions = mySort(board, pre_actions, color)
        for i in range(0, len(actions)):
            value = max(value,
                        alphabeta_min_node(play_move(board, color, actions[i][0], actions[i][1]), oppositecolor, alpha,
                                           beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        board_dict[board] = value
        return value


def select_move_alphabeta(board, color):
    if color == 1:
        oppositecolor = 2
    else:
        oppositecolor = 1
    alpha = float('-inf')
    beta = float('inf')
    pre_actions = get_possible_moves(board, color)
    actions = mySort(board, pre_actions, color)
    bestvalue = float('-inf')
    bestmove = actions[0]
    for i in range(0, len(actions)):
        if (play_move(board, color, actions[i][0], actions[i][1]) in board_dict):
            currentvalue = board_dict[play_move(board, color, actions[i][0], actions[i][1])]
        else:
            currentvalue = alphabeta_min_node(play_move(board, color, actions[i][0], actions[i][1]), oppositecolor,
                                              alpha, beta)
        if currentvalue > bestvalue:
            bestvalue = currentvalue
            bestmove = actions[i]
    return bestmove


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Minimax AI")  # First line is the name of this AI
    color = int(input())  # Then we read the color: 1 for dark (goes first),
    # 2 for light.

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            # movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()

