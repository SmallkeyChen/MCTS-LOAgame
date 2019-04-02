from LOAState import LOAState
from MCTSNode import MCTSNode
from MCTS import MCTS
import numpy as np

import pygame
import pygame.font
from pygame.locals import *
import sys


def pygame_init():
    pygame.init()
    pygame.display.set_caption("Alpha_Dog")
    screen = pygame.display.set_mode([1100, 900])
    return screen


def draw_chessboard(screen, board, mode):
    """
    :param screen: the pygame surface
    :param board: the np.array we should paint
    :param mode: one mode of three
    """
    screen.fill((233, 204, 138))
    outer_frame_color = (60, 20, 0)
    pygame.draw.rect(screen, outer_frame_color, [80, 80, 740, 740], 5)
    for i in range(1, 10):
        pygame.draw.line(screen, outer_frame_color, (90, 90 * i), (810, 90 * i), 2)
    for i in range(1, 10):
        pygame.draw.line(screen, outer_frame_color, (90 * i, 90), (90 * i, 810), 2)

    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                pygame.draw.circle(screen, (0, 0, 0), ((j+1)*90+45, (i+1)*90+45), 30)
            elif board[i][j] == -1:
                pygame.draw.circle(screen, (255, 255, 255), ((j+1)*90+45, (i+1)*90+45), 30)

    button_color = (163, 80, 21)
    pygame.draw.rect(screen, button_color, [880, 530, 150, 80], 5)
    pygame.draw.rect(screen, button_color, [880, 630, 150, 80], 5)
    pygame.draw.rect(screen, button_color, [880, 730, 150, 80], 5)

    pygame.draw.rect(screen, button_color, [880, 400, 25, 25], 3)
    pygame.draw.rect(screen, button_color, [880, 440, 25, 25], 3)
    pygame.draw.rect(screen, button_color, [880, 480, 25, 25], 3)

    s_font = pygame.font.SysFont("arial", 45)
    text1 = s_font.render("Start", True, button_color)
    text2 = s_font.render("Back", True, button_color)
    text3 = s_font.render("Quit", True, button_color)
    s_font = pygame.font.SysFont("arial", 35)
    p1 = s_font.render("Computer1", True, button_color)
    p2 = s_font.render("Player", True, button_color)
    choose_font = pygame.font.SysFont("arial", 20)
    text4 = choose_font.render("Computer fisrt", True, button_color)
    text5 = choose_font.render("Human fisrt", True, button_color)
    text6 = choose_font.render("Both computer", True, button_color)
    screen.blit(text1, (900, 530))
    screen.blit(text2, (900, 630))
    screen.blit(text3, (900, 730))
    screen.blit(text4, (920, 400))
    screen.blit(text5, (920, 440))
    screen.blit(text6, (920, 480))
    screen.blit(p1, (850, 160))
    screen.blit(p2, (850, 260))
    if mode == 1:
        pygame.draw.rect(screen, (0, 255, 0), [883, 403, 19, 19])
    elif mode == 2:
        pygame.draw.rect(screen, (0, 255, 0), [883, 443, 19, 19])
    elif mode == 3:
        pygame.draw.rect(screen, (0, 255, 0), [883, 483, 19, 19])
    pygame.display.update()


def draw_focusbox(screen, focus):
    x_ = focus[0]
    y_ = focus[1]
    pygame.draw.rect(screen, (0, 255, 0), [x_, y_, 68, 68], 4)
    pygame.display.update()
    return screen


def draw_time(screen, time1, time2):
    # s_font = pygame.font.SysFont("arial", 35)
    # t1 = s_font.render(time1, True, (255, 0, 0))
    # screen.blit(t1, (850, 160))
    # t2 = s_font.render(time2, True, (255, 0, 0))
    # screen.blit(t2, (850, 160))
    # return screen
    pass


def draw_countdown(screen, count):
    pygame.draw.rect(screen, (233, 204, 138), [880, 10, 120, 100])
    s_font = pygame.font.SysFont("arial", 100)
    t1 = s_font.render(str(count), True, (255, 0, 0))
    screen.blit(t1, (900, 50))
    pygame.display.update()
    return screen


def computer_fisrt(screen, state):
    count = 60
    focus = None
    focused = False
    has_chess = False
    # pygame.time.set_timer(11, 1000)
    root = MCTSNode(state)
    state = MCTS.best_action(5, root).state
    draw_chessboard(screen, state.board, 1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = int(x / 90) - 1
                row = int(y / 90) - 1
                if 80 < x < 820 and 80 < y < 820:
                    if state.board[row][col] == -1:
                        focused = True
                        focus = (row, col)
                        draw_focusbox(screen, ((col + 1) * 90 + 10, (row + 1) * 90 + 10))
                    elif state.board[row][col] != -1 and focused:
                        focused = False
                        goto = (row, col)
                        if state.is_move_legal([focus, goto]):
                            state = state.state_move([focus, goto])
                            draw_chessboard(screen, state.board, 1)
                            has_chess = True
                        if has_chess:
                            root = MCTSNode(state)
                            state = MCTS.best_action(5, root).state
                            draw_chessboard(screen, state.board, 1)
                            has_chess = False
                        # draw_countdown(screen, count)
                if 880 < x < 1030 and 300 < y < 400:
                    return

            # if event.type == 11:
            #     count = count - 1
            #     draw_countdown(screen, count)
            #     if count == 0:
            #         if state.now_move == 1:
            #             return -1
            #         else:
            #             return 1


if __name__ == "__main__":
    screen = pygame_init()
    initial_board = np.zeros((8, 8))
    initial_board[[0, 7], 1:7] = 1
    initial_board[1:7, [0, 7]] = -1
    state = LOAState(initial_board, 1)
    is_end = True
    global_moves = []
    mode = 1
    count = 60
    draw_chessboard(screen, initial_board, mode)
    draw_countdown(screen, count)

    computer_time = 0
    player_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 880 < x < 1030 and 530 < y < 610 and is_end:
                    is_end = False
                    computer_fisrt(screen, state)
                    is_end = True

                if 880 < x < 905 and is_end:
                    if 400 < y < 425:
                        mode = 1
                    elif 440 < y < 465:
                        mode = 2
                    elif 480 < y < 505:
                        mode = 3
                    draw_chessboard(screen, initial_board, mode)
                    draw_countdown(screen, count)









