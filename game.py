from grid import Grid
from blocks import *
import random 
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
        if self.block_inside() == False or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            self.grid.grid[tile.row][tile.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        self.grid.clear_full_rows()
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
        self.current_block.draw(screen)