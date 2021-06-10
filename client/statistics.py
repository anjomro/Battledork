import numpy as np


class Statistics:
    curve = []

    def __init__(self, ball_curve):
        self.curve = ball_curve

    def count_hits(self):
        last_position = self.curve[0]
        hits = 0
        # Iterate over curve to find changes in direction
        for position in self.curve[1:]:
            # y coordinate will be zero if ball was not found
            # if ball is directly over the net, check if it crosses in next step
            if position[1] == 0:
                continue
            # Detect if ball crossed the net
            # multiplied y coordinates will be negative if ball crossed the net
            if last_position[1] * position[1] < 0:
                hits += 1
            last_position = position
        return hits
