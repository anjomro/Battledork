import numpy as np


class Statistics:
    curve = []

    def __init__(self, ball_curve):
        self.curve = ball_curve

    def count_hits(self):
        last_position = self.curve[0]
        direction = 0
        hits = 0
        # Iterate over curve to find changes in direction
        for position in self.curve[1:]:
            if position == np.array([[0], [0], [-10]]):
                continue
            # New direction either positive or negative
            new_direction = (position[1]-last_position[1] > 0)
            # If new direction is different, count a hit
            if new_direction != direction:
                hits += 1
                direction = new_direction
        return hits
