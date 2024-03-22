import pygame
import random
from pygame.locals import *


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
    
class MemoryGame:
    def __init__(self, frame_speed=30, speed_reveal = 8):
        pygame.init()
        self.frame_speed = frame_speed
        self.window_width = 540
        self.window_height = 380
        self.speed_reveal = speed_reveal
        self.box_size = 50
        self.gap_size = 15
        self.border_width = 4
        self.border_height = 4
        self.x_margin = int((self.window_width - (self.border_width * (self.box_size + self.gap_size))) / 2)
        self.y_margin = int((self.window_height - (self.border_height * (self.box_size + self.gap_size))) / 2)
        self.background_color = (100, 100, 100)
        self.light_background_color = (60, 60, 100)
        self.box_color = (0, 255, 255)
        self.highlight_color = (255, 255, 0)
        # DIS_PlaySurf
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Memory Game')
        self.frame_speed_clock = pygame.time.Clock()
        self.board = RandomizedBoard(self.border_width, self.border_height).board
        #Boxes_revealed
        self.boxes_revealed = self.generate_data_revealed_boxes(False)
        self.first_selection = None