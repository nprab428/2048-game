import tkinter as tk
import tkinter.messagebox as msg
import random

CELL_LENGTH = 100
PADDING_PERCENT = .20
PADDING = CELL_LENGTH * PADDING_PERCENT


class GameBoard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('2048 Game')
        window_length = int(4*CELL_LENGTH + 5*PADDING)
        self.geometry(f'{window_length}x{window_length}')

        self.canvas = tk.Canvas(
            self, bg='#BAADA1', highlightthickness=0, relief='ridge')
        self.canvas.pack(fill=tk.BOTH, expand=1)

        # 2D array to store cells as a grid
        self.cells = [[0 for i in range(4)] for j in range(4)]
        # create cells in COLUMN MAJOR order
        for i in range(4):
            for j in range(4):
                x1 = i*CELL_LENGTH + (i+1)*PADDING
                y1 = j*CELL_LENGTH + (j+1)*PADDING
                x2 = (i+1)*CELL_LENGTH + (i+1)*PADDING
                y2 = (j+1)*CELL_LENGTH + (j+1)*PADDING
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill='#CCC1B5', width=0)
                # store all cells as initially empty
                self.cells[i][j] = {
                    'canvas_coords': (x1, y1), 'tile': None, 'tile_window': None}

        self.bind('<Right>', lambda event,
                  dir='R': self.handle_move(dir))
        self.bind('<Left>', lambda event,
                  dir='L': self.handle_move(dir))
        self.bind('<Down>', lambda event,
                  dir='D': self.handle_move(dir))
        self.bind('<Up>', lambda event,
                  dir='U': self.handle_move(dir))

        # create new game
        self.new_game()

    def new_game(self):
        for i in range(4):
            for j in range(4):
                self.cells[i][j]['tile'] = None
                self.cells[i][j]['tile_window'] = None

        self.canvas.delete('tile')
        for i in range(2):
            self.insert_new_tile()

    def insert_new_tile(self, testing=False):
        PERCENTAGE_IS_TWO = .89
        value = 4 if random.random() > PERCENTAGE_IS_TWO else 2
        tile = Tile(self.canvas, value)

        empty_cells = [(i, j, cell) for i, col in enumerate(self.cells)
                       for j, cell in enumerate(col) if not cell['tile']]
        c = random.choice(empty_cells)
        tile_window = self.canvas.create_window(
            c[2]['canvas_coords'], window=tile, anchor=tk.NW, width=CELL_LENGTH, height=CELL_LENGTH, tags='tile')
        self.cells[c[0]][c[1]]['tile'] = tile
        self.cells[c[0]][c[1]]['tile_window'] = tile_window
        self.canvas.update()

        if self.is_game_over():
            if msg.askokcancel('Game over', 'There are no more moves left!\n\nWould you like to play again?'):
                self.new_game()

    def is_game_over(self):
        empty_cells = [
            (i, j, cell) for i, col in enumerate(self.cells) for j, cell in enumerate(col) if not cell['tile']]
        if len(empty_cells) == 0:
            # if there are adjacent tiles with same values, then a move exists
            # check along cols
            for i in range(4):
                for j in range(3):
                    if self.cells[i][j]['tile'].value == self.cells[i][j+1]['tile'].value:
                        return False
            # check along rows
            for i in range(3):
                for j in range(4):
                    if self.cells[i][j]['tile'].value == self.cells[i+1][j]['tile'].value:
                        return False
            # if we get here then no move exists
            return True
        # empty cell is present, so a move exists
        return False

    def handle_move(self, dir):
        move_occured = False
        iterators = {'R': {'i': list(reversed(range(3))), 'j': list(range(4))},
                     'L': {'i': list(range(1, 4)), 'j': list(range(4))},
                     'D': {'i': list(range(4)), 'j': list(reversed(range(3)))},
                     'U': {'i': list(range(4)), 'j': list(range(1, 4))}}

        for i in iterators[dir]['i']:
            for j in iterators[dir]['j']:
                if self.cells[i][j]['tile']:
                    target_i, target_j = self.compute_target(i, j, dir)
                    if self.place_tile(i, j, target_i, target_j):
                        move_occured = True
                    else:
                        prev_i, prev_j = self._get_prev_cell(
                            target_i, target_j, dir)
                        if (prev_i, prev_j) != (i, j):  # move is possible
                            self.place_tile(i, j, prev_i, prev_j)
                            move_occured = True
        if move_occured:
            self.insert_new_tile()

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

    def compute_target(self, i, j, dir):
        if dir not in ['L', 'R', 'U', 'D']:
            raise ValueError("Invalid argument for dir")
        if dir == 'R':
            target_i = i+1
            while target_i < 3 and not self.cells[target_i][j]['tile']:
                target_i += 1
            return target_i, j
        elif dir == 'L':
            target_i = i-1
            while target_i > 0 and not self.cells[target_i][j]['tile']:
                target_i -= 1
            return target_i, j
        elif dir == 'D':
            target_j = j+1
            while target_j < 3 and not self.cells[i][target_j]['tile']:
                target_j += 1
            return i, target_j
        else:  # U
            target_j = j-1
            while target_j > 0 and not self.cells[i][target_j]['tile']:
                target_j -= 1
            return i, target_j

    def place_tile(self, orig_i, orig_j, dest_i, dest_j):
        orig_cell = self.cells[orig_i][orig_j]
        dest_cell = self.cells[dest_i][dest_j]
        orig_value = orig_cell['tile'].value
        dest_value = None

        if dest_cell['tile']:
            dest_value = dest_cell['tile'].value

        # 3 cases for placement
        if not dest_cell['tile']:
            self.move_tile(orig_i, orig_j, dest_i, dest_j)
            return True
        elif orig_value == dest_value:
            old_tile_window = dest_cell['tile_window']
            self.move_tile(orig_i, orig_j, dest_i, dest_j)
            dest_cell['tile'].double_value()
            self.canvas.delete(old_tile_window)
            return True
        else:
            return False

    def move_tile(self, orig_i, orig_j, dest_i, dest_j):
        DELTA = CELL_LENGTH + PADDING
        DELAY = 1  # ms
        dx = dy = di = dj = 0

        if dest_i > orig_i and dest_j == orig_j:  # right
            dx = DELTA
            di = 1
            dir = 'R'
        elif dest_i < orig_i and dest_j == orig_j:  # left
            dx = -DELTA
            di = -1
            dir = 'L'
        elif dest_i == orig_i and dest_j > orig_j:  # down
            dy = DELTA
            dj = 1
            dir = 'D'
        elif dest_i == orig_i and dest_j < orig_j:  # up
            dy = -DELTA
            dj = -1
            dir = 'U'
        else:
            raise ValueError('Moves must be right, left, down, or up')

        tile_window = self._move_one_unit(orig_i, orig_j, di, dj, dx, dy)
        curr_canvas_i, curr_canvas_j = self.canvas.coords(tile_window)
        dest_canvas_i, dest_canvas_j = self.cells[dest_i][dest_j]['canvas_coords']
        if dir == 'R':
            if curr_canvas_i < dest_canvas_i:
                self.canvas.after(DELAY, self.move_tile(
                    orig_i + 1, orig_j, dest_i, dest_j))
        elif dir == 'L':
            if curr_canvas_i > dest_canvas_i:
                self.canvas.after(DELAY, self.move_tile(
                    orig_i - 1, orig_j, dest_i, dest_j))
        elif dir == 'D':
            if curr_canvas_j < dest_canvas_j:
                self.canvas.after(DELAY, self.move_tile(
                    orig_i, orig_j+1, dest_i, dest_j))
        else:  # U
            if curr_canvas_j > dest_canvas_j:
                self.canvas.after(DELAY, self.move_tile(
                    orig_i, orig_j-1, dest_i, dest_j))

    def _move_one_unit(self, orig_i, orig_j, di, dj, dx, dy):
        orig_cell = self.cells[orig_i][orig_j]
        dest_cell = self.cells[orig_i + di][orig_j + dj]
        tile_window = orig_cell['tile_window']

        self.canvas.move(tile_window, dx, dy)
        dest_cell['tile'] = orig_cell['tile']
        dest_cell['tile_window'] = orig_cell['tile_window']
        orig_cell['tile'] = orig_cell['tile_window'] = None
        self.canvas.update()
        return tile_window


class Tile(tk.Frame):
    def __init__(self, master, value=2):
        super().__init__(master)
        self._valueVar = tk.IntVar(self, 0)
        self.tile = tk.Label(self, textvar=self._valueVar,
                             font=('arial', 60, 'bold'))

        self._set_value(value)
        self.color_mapping = {2: {'bg': '#EEE4DB', 'fg': '#766E66'},
                              4: {'bg': '#EEDFC9', 'fg': '#766E66'},
                              8: {'bg': '#F1B17D', 'fg': '#F6FEFE'},
                              16: {'bg': '#EA8D5B', 'fg': '#F6FEFE'},
                              32: {'bg': '#F57B63', 'fg': '#F6FEFE'},
                              64: {'bg': '#E85B3F', 'fg': '#F6FEFE'},
                              128: {'bg': '#ECCE78', 'fg': '#F6FEFE'},
                              256: {'bg': '#ECCB69', 'fg': '#F6FEFE'},
                              512: {'bg': '#ECC75A', 'fg': '#F6FEFE'},
                              1024: {'bg': '#ECC44C', 'fg': '#F6FEFE'},
                              2048: {'bg': '#EBC32C', 'fg': '#F6FEFE'}}
        self._color_tile()
        self.tile.pack(fill=tk.BOTH, expand=1)

    @property
    def value(self):
        return self._valueVar.get()

    def _set_value(self, value):
        self._valueVar.set(value)
        # check if need to downsize font
        if len(str(self.value)) == 3:
            self.tile.configure(font=('arial', 50, 'bold'))
        if len(str(self.value)) == 4:
            self.tile.configure(font=('arial', 40, 'bold'))

    def double_value(self):
        self._set_value(self.value*2)
        self._color_tile()

    def _color_tile(self):
        self.tile.configure(bg=self.color_mapping[self.value]['bg'],
                            fg=self.color_mapping[self.value]['fg'])


if __name__ == "__main__":
    game_board = GameBoard()
    game_board.mainloop()
