import pygame
from pygame.locals import *
import random
import sys

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
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Memory Game')
        self.frame_speed_clock = pygame.time.Clock()
        self.board = RandomizedBoard(self.border_width, self.border_height).board
        self.boxes_revealed = self.generate_data_revealed_boxes(False)
        self.first_selection = None

    def generate_data_revealed_boxes(self, val):
        boxes_revealed = []
        for i in range(self.border_width):
            boxes_revealed.append([val] * self.border_height)
        return boxes_revealed
    
    def split_groups(self, group_Size, List):
        result = []
        for i in range(0, len(List), group_Size):
            result.append(List[i:i + group_Size])
        return result
    
    def lef_top_coord(self, x_box, y_box):
        left = x_box * (self.box_size + self.gap_size) + self.x_margin
        top = y_box * (self.box_size + self.gap_size) + self.y_margin
        return (left, top)
    
    def get_shape_color(self, x_box, y_box):
        return (self.board[x_box][y_box][0], self.board[x_box][y_box][1])
    
    def draw_icon(self, shape:str, color, left, top):
        quarter = int(self.box_size * 0.25) 
        half    = int(self.box_size * 0.5)   
        if 'circle' == shape.lower():
            pygame.draw.circle(self.screen, color, (left + half, top + half), half - 5)
            pygame.draw.circle(self.screen, self.background_color, (left + half, top + half), quarter - 5)
        elif 'square' == shape.lower():
            pygame.draw.rect(self.screen, color, (left + quarter, top + quarter, half, half))
        elif 'diamond' == shape.lower():
            pygame.draw.polygon(self.screen, color, ((left + half, top), (left + self.box_size - 1, top + half), (left + half, top + self.box_size - 1), (left, top + half)))
        elif 'lines' == shape.lower():
            for i in range(0, self.box_size, 4):
                pygame.draw.line(self.screen, color, (left, top + i), (left + i, top))
                pygame.draw.line(self.screen, color, (left + i, top + self.box_size - 1), (left + self.box_size - 1, top + i))
        elif 'oval' == shape.lower():
            pygame.draw.ellipse(self.screen, color, (left, top + quarter, self.box_size, half))

    # Draws all of the boxes in their covered or revealed state.
    def draw_board(self, revealed):
        for x_box in range(self.border_width):
            for y_box in range(self.border_height):
                left, top = self.lef_top_coord(x_box, y_box)
                if not revealed[x_box][y_box]:                
                    pygame.draw.rect(self.screen, self.box_color, (left, top, self.box_size, self.box_size))
                else:
                    shape, color = self.get_shape_color(x_box, y_box)
                    self.draw_icon(shape, color, left, top)

    #Revealing and covering animation
    def reveal_boxes(self, boxesToReveal):
        for coverage in range(self.box_size, (-self.speed_reveal) - 1, -self.speed_reveal):
            self.box_cover(boxesToReveal, coverage)
    
    def cover_boxes(self, boxesToCover):
        for coverage in range(0, self.box_size + self.speed_reveal, self.speed_reveal):
            self.box_cover(boxesToCover, coverage)
    
    def box_cover(self, boxes, coverage):
        for box in boxes:
            left, top = self.lef_top_coord(box[0], box[1])
            pygame.draw.rect(self.screen, self.background_color, (left, top, self.box_size, self.box_size))
            shape, color = self.get_shape_color( box[0], box[1])
            self.draw_icon(shape, color, left, top)

            if coverage > 0: # only draw the cover if there is an coverage
                pygame.draw.rect(self.screen, self.box_color, (left, top, coverage, self.box_size))
        pygame.display.update()
        self.frame_speed_clock.tick(self.frame_speed)

    def start_game(self):
        boxes_not_revealed = self.generate_data_revealed_boxes(False)
        boxes = []
        for x in range(self.border_width):
            for y in range(self.border_height):
                boxes.append( (x, y) )
        random.shuffle(boxes)

        box_Groups = self.split_groups(8, boxes)
        self.draw_board(boxes_not_revealed)

        for boxGroup in box_Groups:
            self.reveal_boxes(boxGroup)
            self.cover_boxes(boxGroup)

       
    def main(self):
        pygame.init()
        self.screen.fill(self.background_color)
        self.start_game()
        
if __name__ == '__main__':
    game = MemoryGame()
    game.main()