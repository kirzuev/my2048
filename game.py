# coding: utf-8

import pygame
import random
import numpy as np

def val_to_color(val):
    if val == None:
        return (238, 228, 218, 0.35)
    else:
        r = 255
        g = 255 - int(255 * np.log2(val) / np.log2(2048))
        b = 0
        return (r, g, b, 0.5)

class Game:
    def __init__(self, size=(4,4)):
        self.best_score = 0
        self.new(size)
        self.button = pygame.Rect(40, 120, size[1] * 100 - 80, 60)

    def new(self, size=(4,4)):
        self.score = 0
        self.size = size
        self.is_changed = False
        self.is_playing = True
        available_cells = []
        field = []
        for i in range(size[0]):
            row = []
            for j in range(size[1]):
                row.append(Cell())
                available_cells.append((i, j))
            field.append(row)
        cell1 = random.choice(available_cells)
        available_cells.remove(cell1)
        cell2 = random.choice(available_cells)
        available_cells.remove(cell2)
        val1 = random.choice([2,2,4])
        val2 = random.choice([2,2,4])
        i, j = cell1
        field[i][j] = Cell(val1)
        i, j = cell2
        field[i][j] = Cell(val2)
        self.available_cells = available_cells  
        self.field = field

    def draw_header(self, screen):
        font_size = 24
        dark_color = (119, 110, 101)
        light_color = (250, 248, 239)
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        score_text = font.render('SCORE: ' + str(self.score), True, dark_color)
        best_score_text = font.render('BEST: ' + str(self.best_score), True, dark_color)
        screen.blit(score_text, (50, score_text.get_height() // 2))
        screen.blit(best_score_text, (50, 50 + (best_score_text.get_height() // 2)))
        pygame.draw.rect(screen, dark_color, self.button)
        button_text = font.render('NEW GAME', True, light_color)
        button_text_rect = button_text.get_rect()
        button_text_rect.center = self.button.center
        screen.blit(button_text, button_text_rect)

    def draw(self, screen):
        n, m = self.size
        bg_color = (250, 248, 239)
        screen.fill(bg_color)
        self.draw_header(screen)
        field_color = (187, 173, 160)
        field_height = n * 100
        field_width = m * 100
        pygame.draw.rect(screen, field_color, pygame.Rect(0, 200, field_width, field_height))
        dark_color = (119, 110, 101)
        light_color = bg_color
        font_size = 36
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        for i in range(n):
            for j in range(m):
                cell = self.field[i][j]
                x = 10 + 100 * j
                y = 200 + 10 + 100 * i
                cell_rect = pygame.Rect(x, y, 80, 80)
                pygame.draw.rect(screen, cell.color, cell_rect)
                if not cell.is_empty():
                    if cell.val < 8:
                        font_color = dark_color
                    else:
                        font_color = light_color
                    cell_text = font.render(str(cell.val), True, font_color)
                    cell_text_rect = cell_text.get_rect()
                    cell_text_rect.center = cell_rect.center
                    screen.blit(cell_text, cell_text_rect)     

    def win(self):
        for row in self.field:
            for cell in row:
                if cell.val == 2048:
                    return True
        return False

    def win_screen(self, screen):
        self.is_playing = False
        n, m = self.size
        field_color = (187, 173, 160)
        field_height = n * 100
        field_width = m * 100
        field = pygame.Rect(0, 200, field_width, field_height)
        pygame.draw.rect(screen, field_color, field)
        font_size = 24
        font_color = (250, 248, 239)
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        win_text = font.render('YOU WIN!', True, font_color)
        win_text_rect = win_text.get_rect()
        win_text_rect.center = field.center
        screen.blit(win_text, win_text_rect)

    def lose(self):
        if len(self.available_cells) > 0:
            return False
        n, m = self.size
        for i in range(n):
            for j in range(m-1):
                current_val = self.field[i][j].val
                next_val = self.field[i][j+1].val
                if current_val == next_val:
                    return False
        for j in range(m):
            for i in range(n-1):
                current_val = self.field[i][j].val
                next_val = self.field[i+1][j].val
                if current_val == next_val:
                    return False
        return True
    
    def lose_screen(self, screen):
        self.is_playing = False
        n, m = self.size
        field_color = (187, 173, 160)
        field_height = n * 100
        field_width = m * 100
        field = pygame.Rect(0, 200, field_width, field_height)
        pygame.draw.rect(screen, field_color, field)
        font_size = 24
        font_color = (250, 248, 239)
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        lose_text = font.render('YOU LOSE', True, font_color)
        lose_text_rect = lose_text.get_rect()
        lose_text_rect.center = field.center
        screen.blit(lose_text, lose_text_rect)
    
    def update_available_cells(self):
        n, m = self.size
        available_cells = []
        for i in range(n):
            for j in range(m):
                if self.field[i][j].is_empty():
                    available_cells.append((i, j))
        self.available_cells = available_cells

    def new_cell(self):
        cell = random.choice(self.available_cells)
        self.available_cells.remove(cell)        
        val = random.choice([2,4])
        i, j = cell
        self.field[i][j] = Cell(val)

    def update_score(self, val):
        self.score += val
        if self.score > self.best_score:
            self.best_score = self.score    

    def move_up(self):
        n, m = self.size        
        for j in range(m):
            for i in range(1, n):
                if self.field[i][j].is_empty():
                    continue
                new_i = i - 1
                if self.field[new_i][j].is_empty():
                    while new_i >= 0 and self.field[new_i][j].is_empty():
                        new_i -= 1
                    new_i += 1
                    self.field[new_i][j] = self.field[i][j]
                    self.field[i][j] = Cell()
                    self.is_changed = True

    def merge_up(self):
        n, m = self.size        
        for j in range(m):
            for i in range(n-1):
                current_val = self.field[i][j].val
                next_val = self.field[i+1][j].val
                if current_val != None and current_val == next_val:
                    self.field[i][j].merge()
                    self.field[i+1][j] = Cell()
                    self.is_changed = True
                    self.update_score(current_val * 2)

    def up(self):
        self.is_changed = False        
        self.move_up()
        self.merge_up()
        self.move_up()
        if self.is_changed:
            self.update_available_cells()
            self.new_cell()

    def move_down(self):
        n, m = self.size
        for j in range(m):
            for i in range(n-2, -1, -1):
                if self.field[i][j].is_empty():
                    continue
                new_i = i + 1
                if self.field[new_i][j].is_empty():
                    while new_i < n and self.field[new_i][j].is_empty():
                        new_i += 1
                    new_i -= 1
                    self.field[new_i][j] = self.field[i][j]
                    self.field[i][j] = Cell()
                    self.is_changed = True

    def merge_down(self):
        n, m = self.size
        for j in range(m):
            for i in range(n-1, 0, -1):
                current_val = self.field[i][j].val
                next_val = self.field[i-1][j].val
                if current_val != None and current_val == next_val:
                    self.field[i][j].merge()
                    self.field[i-1][j] = Cell()
                    self.is_changed = True
                    self.update_score(current_val * 2)

    def down(self):
        self.is_changed = False        
        self.move_down()
        self.merge_down()
        self.move_down()
        if self.is_changed:
            self.update_available_cells()
            self.new_cell()

    def move_left(self):
        n, m = self.size        
        for i in range(n):
            for j in range(1, m):
                if self.field[i][j].is_empty():
                    continue
                new_j = j - 1
                if self.field[i][new_j].is_empty():
                    while new_j >= 0 and self.field[i][new_j].is_empty():
                        new_j -= 1
                    new_j += 1
                    self.field[i][new_j] = self.field[i][j]
                    self.field[i][j] = Cell()
                    self.is_changed = True

    def merge_left(self):
        n, m = self.size
        for i in range(n):
            for j in range(m-1):
                current_val = self.field[i][j].val
                next_val = self.field[i][j+1].val
                if current_val != None and current_val == next_val:
                    self.field[i][j].merge()
                    self.field[i][j+1] = Cell()
                    self.is_changed = True
                    self.update_score(current_val * 2)

    def left(self):
        self.is_changed = False
        self.move_left()
        self.merge_left()
        self.move_left()
        if self.is_changed:
            self.update_available_cells()
            self.new_cell()

    def move_right(self):
        n, m = self.size
        for i in range(n):
            for j in range(m-2, -1, -1):
                if self.field[i][j].is_empty():
                    continue
                new_j = j + 1
                if self.field[i][new_j].is_empty():
                    while new_j < m and self.field[i][new_j].is_empty():
                        new_j += 1
                    new_j -= 1
                    self.field[i][new_j] = self.field[i][j]
                    self.field[i][j] = Cell()
                    self.is_changed = True

    def merge_right(self):
        n, m = self.size
        for i in range(n):
            for j in range(m-1, 0, -1):
                current_val = self.field[i][j].val
                next_val = self.field[i][j-1].val
                if current_val != None and current_val == next_val:
                    self.field[i][j].merge()
                    self.field[i][j-1] = Cell()
                    self.is_changed = True
                    self.update_score(current_val * 2)

    def right(self):
        self.is_changed = False
        self.move_right()
        self.merge_right()
        self.move_right()
        if self.is_changed:
            self.update_available_cells()
            self.new_cell()

class Cell:
    def __init__(self, val=None):
        self.val = val
        self.color = val_to_color(val)

    def is_empty(self):
        return self.val == None

    def merge(self):
        val = self.val * 2
        self.val = val
        self.color = val_to_color(val)

pygame.init()
pygame.display.init()
pygame.display.set_caption('2048')

size = (4, 4)
n, m = size
height = n * 100 + 200
width = m * 100
screen = pygame.display.set_mode((width, height))

game = Game(size)

while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break
        if game.is_playing:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                game.up()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                game.down()
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                game.left()
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                game.right()
        if event.key == pygame.K_r:
            game.new()
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if game.button.collidepoint(event.pos):
            game.new()
    game.draw(screen)
    if game.win():
        game.win_screen(screen)
    elif game.lose():
        game.lose_screen(screen)
    pygame.display.update()

pygame.display.quit()
pygame.quit()
