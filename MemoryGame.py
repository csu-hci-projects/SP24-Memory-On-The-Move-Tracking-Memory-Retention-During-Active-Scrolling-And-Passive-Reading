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
        random.shuffle(icon)
        # slicing
        icon = icon[:self.num_icons_used] * 2
        random.shuffle(icon)
        return [icon[y * self.border_width: (y + 1) * self.border_width] for y in range(self.border_height)]
    
class MemoryGame:
    def __init__(self, speed_reveal = 10):
        pygame.init()
        self.window_width = 540
        self.window_height = 380
        self.speed_reveal = speed_reveal
        self.box_size = 50
        self.gap_size = 15
        self.border_width = 4
        self.border_height = 4
        self.x_margin = int((self.window_width - (self.border_width * (self.box_size + self.gap_size))) / 2)
        self.y_margin = int((self.window_height - (self.border_height * (self.box_size + self.gap_size))) / 2)
        self.background_color = (243, 207, 198)
        self.dark_background_color = (248, 131, 121)
        self.timer_color = (124, 51, 255)
        self.box_color = (5, 209, 252)
        self.highlight_color = (255, 255, 0)
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Memory Game')
        self.font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()
        self.start_time = 0
        self.board = RandomizedBoard(self.border_width, self.border_height).board
        self.boxes_revealed = self.generate_data_revealed_boxes(False)

    def format_time(self, milliseconds):
        seconds = milliseconds // 1000
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    def generate_data_revealed_boxes(self, val):
        boxes_revealed = []
        for i in range(self.border_width):
            boxes_revealed.append([val] * self.border_height)
        return boxes_revealed
       
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
    def reveal_boxes(self, boxesToReveal, frame_rate):
        for coverage in range(self.box_size, (-self.speed_reveal) - 1, -self.speed_reveal):
            self.box_cover(boxesToReveal, coverage, frame_rate)
    
    def cover_boxes(self, boxesToCover, frame_rate):
        for coverage in range(0, self.box_size + self.speed_reveal, self.speed_reveal):
            self.box_cover(boxesToCover, coverage, frame_rate)
    
    def box_cover(self, boxes, coverage, frame_rate):
        for box in boxes:
            left, top = self.lef_top_coord(box[0], box[1])
            pygame.draw.rect(self.screen, self.background_color, (left, top, self.box_size, self.box_size))
            shape, color = self.get_shape_color( box[0], box[1])
            self.draw_icon(shape, color, left, top)

            if coverage > 0: # only draw the cover if there is an coverage
                pygame.draw.rect(self.screen, self.box_color, (left, top, coverage, self.box_size))
        pygame.display.update()
        self.clock.tick(frame_rate)

    def start_game(self):
        pygame.init()
        self.screen.fill(self.background_color)
        boxes = []
        for x in range(self.border_width):
            for y in range(self.border_height):
                boxes.append( (x, y) )
        random.shuffle(boxes)

        self.draw_board(self.boxes_revealed)
        self.reveal_boxes(boxes, 5)
        self.cover_boxes(boxes, 5)

        # Initialize timer
        self.start_time = pygame.time.get_ticks()

    # Converting to pixel coordinates to box coordinates
    def box_pixel(self, x, y):
        for x_box in range(self.border_width):
            for y_box in range(self.border_height):
                left, top = self.lef_top_coord(x_box, y_box)
                box_Rect = pygame.Rect(left, top, self.box_size, self.box_size)
                if box_Rect.collidepoint(x, y):
                    return (x_box, y_box)
        return (None, None)
    
    def is_game_over(self):
        # Returns True if all the boxes have been revealed, otherwise False
        for i in self.boxes_revealed:
            if False in i:
                return False 
        return True
    
    def game_won (self):
        color_1 = self.dark_background_color
        color_2 = self.background_color
        # Calculate elapsed time
        elapsed_time_in_ms = pygame.time.get_ticks() - self.start_time
        elapsed_time = self.format_time(elapsed_time_in_ms) 
        
        for i in range(13):
            color_1, color_2 = color_2, color_1 
            self.screen.fill(color_1)
            self.draw_board(self.boxes_revealed)
            # Render timer text
            timer_text = self.font.render(elapsed_time, True, self.timer_color)
            self.screen.blit(timer_text, (self.window_width // 2 - timer_text.get_width() // 2, 20))
            pygame.display.flip()
            pygame.time.wait(300)
        self.boxes_revealed = self.generate_data_revealed_boxes(False)

    def draw_highlight_box(self, x_box, y_box):
        left, top = self.lef_top_coord(x_box, y_box)
        pygame.draw.rect(self.screen, self.highlight_color, (left - 5, top - 5, self.box_size + 10, self.box_size + 10), 4)
   
    def mouse_coord_event(self, X_mouse, Y_mouse):
        mouse_Clicked = False
        for event in pygame.event.get(): 
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                X_mouse, Y_mouse = event.pos
            elif event.type == MOUSEBUTTONUP:
                X_mouse, Y_mouse = event.pos
                mouse_Clicked = True
        return X_mouse, Y_mouse, mouse_Clicked
    
    def main(self):
        self.start_game()
        X_mouse  = 0 
        Y_mouse = 0 
        first_Selection = None

        while True:    
            X_mouse, Y_mouse, mouse_Clicked = self.mouse_coord_event(X_mouse, Y_mouse)
            x_box, y_box = self.box_pixel(X_mouse, Y_mouse)

            if x_box != None and y_box != None:
                if not self.boxes_revealed[x_box][y_box]:
                    self.draw_highlight_box(x_box, y_box)

                if not self.boxes_revealed[x_box][y_box] and mouse_Clicked:
                    self.reveal_boxes([(x_box, y_box)], self.speed_reveal)
                    self.boxes_revealed[x_box][y_box] = True 
                    if first_Selection == None: 
                        first_Selection = (x_box, y_box)
                    else:
                        icon1shape, icon1color = self.get_shape_color(first_Selection[0], first_Selection[1])
                        icon2shape, icon2color = self.get_shape_color(x_box, y_box)
    
                        if icon1shape != icon2shape or icon1color != icon2color:
                            pygame.time.wait(1000) 
                            self.cover_boxes([(first_Selection[0], first_Selection[1]), (x_box, y_box)], self.speed_reveal)
                            self.boxes_revealed[first_Selection[0]][first_Selection[1]] = False
                            self.boxes_revealed[x_box][y_box] = False
                        elif self.is_game_over(): 
                            self.game_won()
                            pygame.time.wait(2000)
                            return
                           
                        first_Selection = None 

            # Calculate elapsed time
            elapsed_time_in_ms = pygame.time.get_ticks() - self.start_time
            elapsed_time = self.format_time(elapsed_time_in_ms) 
           
            self.screen.fill(self.background_color) 
            self.draw_board(self.boxes_revealed)  

            # Render timer text
            timer_text = self.font.render(elapsed_time, True, self.timer_color)
            self.screen.blit(timer_text, (self.window_width // 2 - timer_text.get_width() // 2, 20))

            pygame.display.flip()
            self.clock.tick(30)
        
if __name__ == '__main__':
    game = MemoryGame()
    game.main()