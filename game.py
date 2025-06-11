from grid import Grid
from blocks import *
import random 
import copy
class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [
            LBlock(),
            JBlock(),
            IBlock(),
            OBlock(),
            SBlock(),
            TBlock()
        ]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [
                LBlock(),
                JBlock(),
                IBlock(),
                OBlock(),
                SBlock(),
                TBlock()
            ]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or not self.block_fits():
            self.current_block.move(0, 1)
    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or not self.block_fits():
            self.current_block.move(0, -1)
    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()
            return False
        return True
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            self.grid.grid[tile.row][tile.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)  
        if self.block_fits() == False:
            self.game_over = True
    def reset(self):
        self.grid.reset()
        self.blocks = [
            LBlock(),
            JBlock(),
            IBlock(),
            OBlock(),
            SBlock(),
            TBlock()
        ]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True
    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or not self.block_fits():
            self.current_block.undo_rotate()
    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True 
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11 ,11)
        if self.next_block.id == 4:
            self.next_block.draw(screen, 336, 320)
        elif self.next_block.id == 3:
            self.next_block.draw(screen, 335, 333)
        else:
            self.next_block.draw(screen, 355, 315)

    
    def get_best_move(self):
        best_score = float('-inf')
        best_col = None
        best_rotation = 0

        for rotation in range(4):
            for col in range(self.grid.num_cols):
                temp_block = copy.deepcopy(self.current_block)
                for _ in range(rotation):
                    temp_block.rotate()
                score = self.simulate_move(temp_block, col)
                if score > best_score:
                    best_score = score
                    best_col = col
                    best_rotation = rotation
        return best_col, best_rotation
    def apply_best_move(self, target_col, target_rotation):
        # Xoay đến rotation mong muốn
        for _ in range(target_rotation):
            self.rotate()
        # Di chuyển trái phải đến cột mong muốn
        max_moves = self.grid.num_cols  # tránh vô tận
        moves = 0
        while self.get_leftmost_column() < target_col and moves < max_moves:
            self.move_right()
            moves += 1
        moves = 0
        while self.get_leftmost_column() > target_col and moves < max_moves:
            self.move_left()
            moves += 1
        # Thả xuống nhanh
        while self.move_down():
            pass    
    # Tính vị trí trái nhất của block hiện tại
    def get_leftmost_column(self):
        return min(tile.column for tile in self.current_block.get_cell_positions())

    # Tương tự tính vị trí phải nhất
    def get_rightmost_column(self):
        return max(tile.column for tile in self.current_block.get_cell_positions())

    def simulate_move(self, block, col_position):
        temp_grid = copy.deepcopy(self.grid)
        positions = block.get_cell_positions()
        block_width = max(tile.column for tile in block.get_cell_positions()) - min(tile.column for tile in block.get_cell_positions()) + 1
        if col_position < 0 or col_position + block_width > temp_grid.num_cols:
            return float('-inf')

        min_col = min(tile.column for tile in block.get_cell_positions())
        while min_col < col_position:
            block.move(0, 1)
            min_col = min(tile.column for tile in block.get_cell_positions())
        while min_col > col_position:
            block.move(0, -1)
            min_col = min(tile.column for tile in block.get_cell_positions())

        while True:
            block.move(1, 0)
            positions = block.get_cell_positions()
            if any(not temp_grid.is_inside(tile.row, tile.column) or not temp_grid.is_empty(tile.row, tile.column) for tile in positions):
                block.move(-1, 0)
                break
        for tile in block.get_cell_positions():
            if 0 <= tile.row < temp_grid.num_rows and 0 <= tile.column < temp_grid.num_cols:
                temp_grid.grid[tile.row][tile.column] = block.id
        rows_cleared = temp_grid.clear_full_rows()
        return temp_grid.evaluate_grid(rows_cleared)