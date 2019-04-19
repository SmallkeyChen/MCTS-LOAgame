from enum import Enum


total_counts = 100      # counts of exploration


# when depth % depth_step == 0, evaluate all legal plays; else evaluate 1/chosen legal plays
depth_step = 5
chosen = 3

depth_threshold = 1000        # when depth > depth_threshold, return evaluation score directly

RollOutMode = Enum('RollOutMode', 'Random Evaluation')
roll_out_mode = RollOutMode.Evaluation


def set_total_counts(x):
    global total_counts
    total_counts = x


def clamp(n, min_n, max_n):
    return max(min(max_n, n), min_n)


MINIMUM_AVERAGE_DIS = [
    0, 0, 2/2, 8/3/3, 4/4, 28/5/5, 9/6, 58/7/7, 10/8,
]