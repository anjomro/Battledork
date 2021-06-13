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

    def max_speed(self, fps):
        max_speed = 0

        for i in range(1, len(self.curve)):
            if (self.curve[i][0] == 0) or (self.curve[i-1][0] == 0):
                continue
            dist = self.curve[i] - self.curve[i-1]
            dist_len = np.sqrt(np.square(dist[0]) + np.square(dist[1]) + np.square(dist[2]))
            speed = dist_len / 100 * fps
            if speed > max_speed:
                max_speed = speed

        return max_speed
