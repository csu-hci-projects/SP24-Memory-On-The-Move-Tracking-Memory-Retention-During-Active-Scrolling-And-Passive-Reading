import random

class RandomizedBoard:
    def __init__(self, num_row_icons, num_col_icons):
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 128, 0), (255, 0, 255), (0, 255, 255)]
        self.shapes = ['circle', 'square', 'diamond', 'lines', 'oval']
        self.border_width = num_row_icons
        self.border_height = num_col_icons
        self.num_icons_used = int(num_row_icons * num_col_icons / 2)
        self.board = self.generate_board()

    def generate_board(self):
        icon = [(shape, color) for color in self.colors for shape in self.shapes]
        icon = icon[:self.num_icons_used] * 2
        random.shuffle(icon)
        return [icon[y * self.border_width: (y + 1) * self.border_width] for y in range(self.border_height)]
