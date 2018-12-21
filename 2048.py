import tkinter as tk
import tkinter.messagebox as msg
import random


class GameBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('2048 Game')
        self.geometry('400x400')

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        self.cells = [[0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                cell = Cell(self, i, j)
                cell.grid(row=i, column=j, sticky='nsew',
                          padx=5, pady=5, ipadx=1, ipady=1)
                self.cells[i][j] = cell

        # self.initialize()
        # For testing, initialize certain cells
        self.cells[0][0].add_tile(2)
        self.cells[0][1].add_tile(2)

        # bind arrow keys
        self.bind("<Right>", self.move_right)
        # self.bind("<Up>", self.move_up)
        # self.bind("<Left>", self.move_left)
        # self.bind("<Down>", self.move_down)

    def initialize(self):
        # insert two tiles
        self.insert_new_tile()
        self.insert_new_tile()

    def insert_new_tile(self):
        if self.is_game_over():
            print('GAME OVER')
            return
        empty_cells = [
            cell for row in self.cells for cell in row if cell.is_empty()]
        random.choice(empty_cells).add_tile(2)

    def is_game_over(self):
        empty_cells = [
            cell for row in self.cells for cell in row if cell.is_empty()]
        if len(empty_cells) == 0:
            # if there are adjacent tiles with same values, then a move exists
            # check along rows
            for i in range(4):
                for j in range(3):
                    if self.cells[i][j].value == self.cells[i][j+1].value:
                        return False
            # check along cols
            for i in range(3):
                for j in range(4):
                    if self.cells[i][j].value == self.cells[i+1][j].value:
                        return False
            # no move exists
            return True
        # empty cell is present
        return False

    def compute_target(self, i, j, direction):
        if direction not in ['L', 'R', 'U', 'D']:
            raise ValueError("Invalid argument for direction")
        if direction == 'R':
            target_j = j+1
            while target_j < 3 and self.cells[i][target_j].is_empty():
                target_j += 1
            return i, target_j

    def place_tile(self, value, i, j):
        if self.cells[i][j].is_empty():
            self.cells[i][j].add_tile(value)
            return True
        elif self.cells[i][j].value == value:
            self.cells[i][j].add_tile(value * 2)
            return True
        else:
            return False

    def move_right(self, event):
        move_occured = False
        for j in reversed(range(3)):
            for i in range(4):
                if not self.cells[i][j].is_empty():
                    value = self.cells[i][j].remove_tile()
                    # assume a move occurs
                    move_occured = True

                    target_i, target_j = self.compute_target(i, j, 'R')
                    if not self.place_tile(value, target_i, target_j):
                        self.cells[target_i][target_j-1].add_tile(value)
                        # now determine if move actually occurs
                        if target_j-1 == j:
                            move_occured = False

        if move_occured:
            self.insert_new_tile()

    # TODO update once implementation is finalized
    # def move_up(self, event):
    #     for i in range(1, 4):
    #         for j in range(4):
    #             if self.cells[i][j].value.get() > 0:
    #                 value = self.cells[i][j].remove_tile()
    #                 self.place_tile(value, i-1, j)

    # def move_left(self, event):
    #     for j in range(1, 4):
    #         for i in range(4):
    #             if self.cells[i][j].value.get() > 0:
    #                 value = self.cells[i][j].remove_tile()
    #                 self.place_tile(value, i, j-1)

    # def move_down(self, event):
    #     for i in reversed(range(3)):
    #         for j in range(4):
    #             if self.cells[i][j].value.get() > 0:
    #                 value = self.cells[i][j].remove_tile()
    #                 self.place_tile(value, i+1, j)


class Cell(tk.Frame):
    def __init__(self, master, x, y):
        super().__init__(master)
        self.x = x
        self.y = y
        # Add default empty tile with a (hidden) dummy value
        self._value = tk.IntVar(self, -1)  # dummy
        self.tile = tk.Label(self, bg="lightgrey",
                             fg="lightgrey", textvar=self._value)
        self.tile.pack(fill=tk.BOTH, expand=1)

        self.color_mapping = {-1: {'bg': 'lightgrey', 'fg': 'lightgrey'},
                              2: {'bg': 'red', 'fg': 'black'},
                              4: {'bg': 'yellow', 'fg': 'black'},
                              8: {'bg': 'orange', 'fg': 'black'},
                              16: {'bg': 'green', 'fg': 'black'},
                              32: {'bg': 'blue', 'fg': 'black'}}

    def add_tile(self, value):
        self._value.set(value)
        self.tile.configure(
            bg=self.color_mapping[value]['bg'], fg=self.color_mapping[value]['fg'])

    def remove_tile(self):
        valueCopy = self.value
        self._value.set(-1)
        self.tile.configure(
            bg=self.color_mapping[-1]['bg'], fg=self.color_mapping[-1]['fg'])
        return valueCopy

    @property
    def value(self):
        return self._value.get() if self._value.get() != -1 else None

    def is_empty(self):
        return self.value is None


if __name__ == "__main__":
    game_board = GameBoard()
    game_board.mainloop()
