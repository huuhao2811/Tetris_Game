import pygame
from colors import Colors
class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 40
        self.grid = [[0 for i in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                print(self.grid[row][col], end=' ')
            print()
    def is_inside(self, row, col):
        if 0 <= row < self.num_rows and 0 <= col < self.num_cols:
            return True
        return False
    def is_empty(self, row, col):
        if self.grid[row][col] == 0:
            return True
        return False
    def is_row_full(self, row):
        for col in range(self.num_cols):
            if self.grid[row][col] == 0:
                return False
        return True
    def clear_row(self, row):
        for col in range(self.num_cols):
            self.grid[row][col] = 0

    def move_rows_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0
    def clear_full_rows(self):
        complete = 0
        for row in range(self.num_rows-1,0,-1):
            if self.is_row_full(row):
                self.clear_row(row)    
                complete += 1
            elif complete > 0:  
                self.move_rows_down(row, complete)
        return complete
    def reset(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.grid[row][col] = 0
    def draw(self,screen):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_value = self.grid[row][col]
                cell_rect = pygame.Rect(col * self.cell_size+11, row * self.cell_size+11, self.cell_size-1, self.cell_size-1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
                pass
    
    def get_grid_metrics(self):
        aggregate_height = 0
        holes = 0
        bumpiness = 0
        heights = []
        
        for col in range(self.num_cols):
            col_height = 0
            found_block = False
            for row in range(self.num_rows):
                if self.grid[row][col] != 0:
                    if not found_block:
                        col_height = self.num_rows - row
                        found_block = True
                elif found_block and self.grid[row][col] == 0:
                    holes += 1
            heights.append(col_height)
            aggregate_height += col_height
        
        for i in range(1, len(heights)):
            bumpiness += abs(heights[i] - heights[i-1])
        return aggregate_height, holes, bumpiness
    
    def evaluate_grid(self, rows_cleared):
        a, b, c, d = -0.510066, 0.760666, -100, -0.184483
        aggregate_height, holes, bumpiness = self.get_grid_metrics()
        print(f"Aggregate Height: {aggregate_height}, Holes: {holes}, Bumpiness: {bumpiness}, Rows Cleared: {rows_cleared}")
        score = (a * aggregate_height) + (b * rows_cleared) + (c * holes) + (d * bumpiness)
        return score
    
