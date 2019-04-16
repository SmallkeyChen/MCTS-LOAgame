total_counts = 300      # counts of exploration

# when depth % depth_step == 0, evaluate all legal plays; else evaluate 1/chosen legal plays
depth_step = 4
chosen = 3

depth_threshold = 80        # when depth > depth_threshold, return evaluation score directly


def set_total_counts(x):
    global total_counts
    total_counts = x

