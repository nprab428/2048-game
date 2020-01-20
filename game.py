import random
import math

from constants import *
from utils import *
from tile import Tile


class TileModel:
    # Holds a tile-sprite and the latest num value assigned to the tile, which
    # may be larger than the num value within the tile-sprite if is_modified is true
    def __init__(self, tile, num):
        self.tile = tile
        self.num = num
        self.is_modified = False

    def double(self):
        self.num *= 2
        self.is_modified = True

    def reset(self):
        self.is_modified = False


class Game:
    def __init__(self, board_cells, all_sprites, map=None):
        self.board_cells = board_cells
        self.all_sprites = all_sprites
        self.map = map

        self.new_game()

    def new_game(self):
        # board_model maintains locations of all active TileModels on board
        self.board_model = [[None] * 4 for _ in range(4)]
        self.all_sprites.empty()

        if self.map:
            self._load_map()
        else:
            for i in range(2):
                self.insert_new_tile()

    def is_game_over(self):
        empty_cells = [
            cell for row in self.board_model for cell in row if not cell]
        if not empty_cells:
            # if there are adjacent tiles with same values, then a move exists
            # check along cols
            for i in range(4):
                for j in range(3):
                    if self.board_model[i][j].num == self.board_model[i][j+1].num:
                        return False
            # check along rows
            for i in range(3):
                for j in range(4):
                    if self.board_model[i][j].num == self.board_model[i+1][j].num:
                        return False
            # if we get here then no move exists
            return True
        # empty cell is present, so a move exists
        return False

    def handle_move(self, dir):
        if dir not in ['L', 'R', 'U', 'D']:
            raise ValueError('Invalid argument for dir')
        moves_queue = []
        iterators = {'R': {'i': list(reversed(range(3))), 'j': list(range(4))},
                     'L': {'i': list(range(1, 4)), 'j': list(range(4))},
                     'D': {'i': list(range(4)), 'j': list(reversed(range(3)))},
                     'U': {'i': list(range(4)), 'j': list(range(1, 4))}}

        # attempt to move all tiles in an order determined by the direction
        for i in iterators[dir]['i']:
            for j in iterators[dir]['j']:
                if self.board_model[i][j]:
                    target_i, target_j = self._compute_target(i, j, dir)
                    move = self._place_tile(i, j, target_i, target_j)
                    if move:
                        moves_queue.append(move)
                    else:
                        prev_i, prev_j = self._get_prev_cell(
                            target_i, target_j, dir)
                        if (prev_i, prev_j) != (i, j):
                            # move is possible to an empty space
                            move = self._place_tile(i, j, prev_i, prev_j)
                            moves_queue.append(move)

        # reset all tile models now that all moves are assigned
        for i in range(4):
            for j in range(4):
                if self.board_model[i][j]:
                    self.board_model[i][j].reset()

        return moves_queue

    def _load_map(self):
        # read lines from file
        lines = []
        with open(self.map, 'r') as map_file:
            for line in map_file:
                lines.append(line)

        # validate dimensions of file
        has_4_cols = all(len(l.split(',')) == 4 for l in lines)
        has_4_rows = len(lines) == 4
        if not has_4_cols or not has_4_rows:
            raise Exception('External map does not have 4x4 dimensions')

        # read contents of file into board (only process powers of 2)
        tile_count = 0
        for j, row in enumerate(lines):
            for i, val in enumerate(row.split(',')):
                tile_num = val.strip()
                if tile_num.isdigit() and math.log2(int(tile_num)).is_integer():
                    tile = Tile(i, j, self.board_cells, int(tile_num))
                    self.board_model[i][j] = TileModel(tile, tile.num)
                    self.all_sprites.add(tile)
                    tile_count += 1

        # validate board is non-empty
        if not tile_count:
            raise Exception('External map contained no valid tiles')

    def _compute_target(self, i, j, dir):
        if dir not in ['L', 'R', 'U', 'D']:
            raise ValueError("Invalid argument for dir")
        if dir == 'R':
            target_i = i+1
            while target_i < 3 and not self.board_model[target_i][j]:
                target_i += 1
            return target_i, j
        elif dir == 'L':
            target_i = i-1
            while target_i > 0 and not self.board_model[target_i][j]:
                target_i -= 1
            return target_i, j
        elif dir == 'D':
            target_j = j+1
            while target_j < 3 and not self.board_model[i][target_j]:
                target_j += 1
            return i, target_j
        else:  # U
            target_j = j-1
            while target_j > 0 and not self.board_model[i][target_j]:
                target_j -= 1
            return i, target_j

    def _place_tile(self, orig_i, orig_j, dest_i, dest_j):
        orig_tile = self.board_model[orig_i][orig_j]
        dest_cell = self.board_model[dest_i][dest_j]

        # Three cases for placement
        # 1) dest cell is empty
        if not dest_cell:
            self.board_model[orig_i][orig_j] = None
            self.board_model[dest_i][dest_j] = orig_tile
            return Move(orig_tile.tile, dest_i, dest_j, absorbing_tile=None)
        # 2) dest value matches orig value meaning they can combine
        if orig_tile.num == dest_cell.num and not dest_cell.is_modified:
            self.board_model[orig_i][orig_j] = None
            self.board_model[dest_i][dest_j].double()
            return Move(orig_tile.tile, dest_i, dest_j, absorbing_tile=dest_cell.tile)
        # 3) dest value doesn't match orig value and thus they can't combine
        return None

    def _get_prev_cell(self, target_i, target_j, dir):
        if dir not in ['L', 'R', 'U', 'D']:
            raise ValueError("Invalid argument for dir")
        if dir == 'R':
            return target_i - 1, target_j
        elif dir == 'L':
            return target_i + 1, target_j
        elif dir == 'D':
            return target_i, target_j - 1
        else:  # 'U'
            return target_i, target_j + 1

    def insert_new_tile(self):
        empty_cells = [(i, j) for i, col in enumerate(self.board_model)
                       for j, tile_model in enumerate(col) if not tile_model]
        x, y = random.choice(empty_cells)

        num = 4 if random.random() > PERCENTAGE_NEW_TILE_IS_TWO else 2
        tile_model = TileModel(Tile(x, y, self.board_cells, num), num)
        self.board_model[x][y] = tile_model
        self.all_sprites.add(tile_model.tile)

    def print_board(self):
        board = [[None] * 4 for _ in range(4)]
        for j, col in enumerate(self.board_model):
            for i, tile in enumerate(col):
                board[i][j] = str(tile.num) if tile else '_'
        return board
