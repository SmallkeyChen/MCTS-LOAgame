from LOAState import LOAState
from MCTSNode import MCTSNode
from MCTS import MCTS
from GlobalVar import *
import numpy as np

import pygame
import pygame.font
from pygame.locals import *
import sys
import threading
import time


def calculate(iters):
    global state, computer1_moved, has_chess, game_terminal
    while not game_terminal:
        if has_chess:
            root = MCTSNode(state)
            node = MCTS.best_action(iters, root)
            if has_chess:
                state = node.state
                computer1_moved = True
                has_chess = False


def computers_cal(iters):
    global state, computer1_moved, computer2_moved, game_terminal
    flag = 1
    # 电脑对战使用同一线程，flag控制交换颜色
    while not game_terminal:
        if flag:
            flag = 1 - flag
            root = MCTSNode(state)
            node = MCTS.best_action(iters, root)
            state = node.state
            computer1_moved = True
        else:
            flag = 1 - flag
            root = MCTSNode(state)
            node = MCTS.best_action(iters, root)
            state = node.state
            computer2_moved = True
        # 需要延时，否则会影响游戏体验
        time.sleep(0.05)


def pygame_init():
    pygame.init()
    pygame.display.set_caption("LOA")
    screen_ = pygame.display.set_mode([1100, 880])
    return screen_


def draw_chessboard(board):
    """
    :param screen: the pygame surface
    :param board: the np.array we should paint
    :param mode: one mode of three
    """
    global screen
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


def draw_focusbox(focus, state):
    global screen
    x_ = (focus[1] + 1) * 90 + 10
    y_ = (focus[0] + 1) * 90 + 10
    pygame.draw.rect(screen, (0, 255, 0), [x_, y_, 68, 68], 4)
    space_row_list, space_col_list = np.where(state.board != state.now_move)
    legal_ends = []
    for e_row, e_col in zip(space_row_list, space_col_list):
        move = [focus, (e_row, e_col)]
        if state.is_move_legal(move):
            legal_ends.append(move[1])
    for point in legal_ends:
        pygame.draw.circle(screen, (0, 255, 0), [(point[1] + 1) * 90 + 45, (point[0] + 1) * 90 + 45], 15)
    pygame.display.update()


def draw_time(time1, time2, now_move=1):
    global screen
    s_font = pygame.font.SysFont("arial", 50)
    m, s = divmod(time1, 60)
    t1 = s_font.render(("%02d:%02d" % (m, s)), True, (255, 0, 0))
    screen.blit(t1, (850, 200))
    m, s = divmod(time2, 60)
    t2 = s_font.render(("%02d:%02d" % (m, s)), True, (255, 0, 0))
    screen.blit(t2, (850, 300))
    if now_move == 1:
        pygame.draw.circle(screen, (0, 0, 0), (1030, 220), 25)
    else:
        pygame.draw.circle(screen, (255, 255, 255), (1030, 320), 25)
    pygame.display.update()


def draw_countdown(count):
    global screen
    pygame.draw.rect(screen, (233, 204, 138), [870, 10, 180, 150])
    s_font = pygame.font.SysFont("arial", 100)
    t1 = s_font.render("%.1f" % count, True, (255, 0, 0))
    screen.blit(t1, (880, 50))
    pygame.display.update()


def draw_computer1win(flag):
    global screen
    s_font = pygame.font.SysFont("arial", 100)
    if flag == 1:
        t1 = s_font.render("Computer1 win!", True, (0, 0, 255))
    elif flag == -1:
        t1 = s_font.render("Computer1 lose!", True, (0, 0, 255))
    else:
        t1 = s_font.render("Game terminal", True, (0, 0, 255))
    screen.blit(t1, (300, 300))
    pygame.display.update()
    time.sleep(2)


def computer():
    global state, computer1_moved, has_chess, count
    computer_time = 0
    player_time = 0
    max_count = count
    global_moves = [state]
    focus = None
    focused = False
    pygame.time.set_timer(18, 100)
    thread_cal = threading.Thread(target=calculate, args=(total_counts, ))
    # args代表best_action迭代次数
    thread_cal.start()

    while True:
        draw_countdown(count)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = int(x / 90) - 1
                row = int(y / 90) - 1
                if 80 < x < 820 and 80 < y < 820 and not has_chess:
                    if state.board[row][col] == -1:
                        focused = True
                        focus = (row, col)
                        draw_chessboard(state.board)
                        draw_countdown(count)
                        draw_time(computer_time, player_time, -1)
                        draw_focusbox(focus, state)
                    elif state.board[row][col] != -1 and focused:
                        goto = (row, col)
                        if state.is_move_legal([focus, goto]):
                            focused = False
                            state = state.state_move([focus, goto])
                            global_moves.append(state)
                            draw_chessboard(state.board)
                            draw_countdown(count)
                            player_time = player_time + max_count - int(count)
                            count = max_count
                            draw_time(computer_time, player_time)
                            has_chess = True

                if 880 < x < 1030 and 730 < y < 810:
                    return 0

                if 880 < x < 1030 and 630 < y < 710:
                    if len(global_moves) > 1:
                        global_moves.pop()
                        state = global_moves[-1]
                        draw_chessboard(state.board)
                        draw_countdown(count)
                        count = max_count
                        draw_time(computer_time, player_time, state.now_move)
                        has_chess = True if state.now_move == 1 else False

            if event.type == 18:
                count = count - 0.1

        if count < 0:
            if state.now_move == 1:
                return -1
            else:
                return 1

        result = state.get_result()
        if result:
            return result

        if computer1_moved:
            computer1_moved = False
            computer_time = computer_time + max_count - int(count)
            count = max_count
            global_moves.append(state)
            draw_chessboard(state.board)
            draw_countdown(count)
            draw_time(computer_time, player_time, -1)


def computers():
    global state, computer1_moved, computer2_moved, count
    computer_time = 0
    player_time = 0
    max_count = count
    pygame.time.set_timer(18, 100)
    thread_cal = threading.Thread(target=computers_cal, args=(total_counts, ))
    thread_cal.start()

    while True:
        draw_countdown(count)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 880 < x < 1030 and 730 < y < 810:
                    return 0
            if event.type == 18:
                count = count - 0.1

        if count < 0:
            if state.now_move == 1:
                return -1
            else:
                return 1

        result = state.get_result()
        if result:
            return result

        if computer1_moved:
            computer1_moved = False
            computer_time = computer_time + max_count - int(count)
            count = max_count
            draw_chessboard(state.board)
            draw_countdown(count)
            draw_time(computer_time, player_time, -1)

        if computer2_moved:
            computer2_moved = False
            player_time = player_time + max_count - int(count)
            count = max_count
            draw_chessboard(state.board)
            draw_countdown(count)
            draw_time(computer_time, player_time, 1)


if __name__ == "__main__":
    screen = pygame_init()
    initial_board = np.zeros((8, 8))
    initial_board[[0, 7], 1:7] = 1
    initial_board[1:7, [0, 7]] = -1
    mode = 1
    now_move = 1
    state = LOAState(initial_board, 1)
    # 默认mode=1，电脑（黑）先下
    count = 60.0
    # 倒计时时间60s
    computer1_moved = False
    computer2_moved = False
    has_chess = None
    game_terminal = None

    draw_chessboard(initial_board)
    draw_countdown(count)
    draw_time(0, 0, 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 880 < x < 1030 and 530 < y < 610:
                    if mode == 1:
                        state = LOAState(initial_board, now_move)
                        has_chess = True

                        game_terminal = False
                        res = computer()
                        game_terminal = True

                        draw_computer1win(res)
                        draw_chessboard(initial_board)
                        count = 60.0
                        draw_countdown(count)
                        draw_time(0, 0, now_move)
                        computer1_moved = False

                    elif mode == 2:
                        state = LOAState(initial_board, now_move)
                        has_chess = False

                        game_terminal = False
                        res = computer()
                        game_terminal = True

                        draw_computer1win(res)
                        draw_chessboard(initial_board)
                        count = 60.0
                        draw_countdown(count)
                        draw_time(0, 0, now_move)
                        computer1_moved = False

                    else:
                        state = LOAState(initial_board, now_move)
                        has_chess = True

                        game_terminal = False
                        res = computers()
                        game_terminal = True

                        draw_computer1win(res)
                        draw_chessboard(initial_board)
                        count = 60.0
                        draw_countdown(count)
                        draw_time(0, 0, now_move)
                        computer1_moved = False

                    draw_chessboard(initial_board)
                    count = 60.0
                    draw_countdown(count)
                    draw_time(0, 0, now_move)

                if 880 < x < 905:
                    if 400 < y < 425:
                        mode = 1
                        now_move = 1
                    elif 440 < y < 465:
                        mode = 2
                        now_move = -1
                    elif 480 < y < 505:
                        mode = 3
                        now_move = 1

                    draw_chessboard(initial_board)
                    count = 60.0
                    draw_countdown(count)
                    draw_time(0, 0, now_move)









