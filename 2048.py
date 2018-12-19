import tkinter as tk


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

        # add test tile
        testCell = self.cells[1][0]
        testCell.add_tile(2)

        # bind arrow keys
        self.bind("<Right>", self.move_right)
        self.bind("<Up>", self.move_up)
        self.bind("<Left>", self.move_left)
        self.bind("<Down>", self.move_down)

    def place_tile(self, value, x, y):
        # TODO - validate if tile can be placed
        self.cells[x][y].add_tile(value)

    def move_right(self, event):
        for j in reversed(range(3)):
            for i in range(4):
                if self.cells[i][j].value.get() > 0:
                    value = self.cells[i][j].remove_tile()
                    self.place_tile(value, i, j+1)

    def move_up(self, event):
        for i in range(1, 4):
            for j in range(4):
                if self.cells[i][j].value.get() > 0:
                    value = self.cells[i][j].remove_tile()
                    self.place_tile(value, i-1, j)

    def move_left(self, event):
        for j in range(1, 4):
            for i in range(4):
                if self.cells[i][j].value.get() > 0:
                    value = self.cells[i][j].remove_tile()
                    self.place_tile(value, i, j-1)

    def move_down(self, event):
        for i in reversed(range(3)):
            for j in range(4):
                if self.cells[i][j].value.get() > 0:
                    value = self.cells[i][j].remove_tile()
                    self.place_tile(value, i+1, j)


class Cell(tk.Frame):
    def __init__(self, master, x, y):
        super().__init__(master)
        self.x = x
        self.y = y
        # Add default empty tile with a (hidden) dummy value
        self.value = tk.IntVar(self, -1)  # dummy
        self.tile = tk.Label(self, bg="lightgrey",
                             fg="lightgrey", textvar=self.value)
        self.tile.pack(fill=tk.BOTH, expand=1)

    def add_tile(self, value):
        self.value.set(value)
        self.tile.configure(bg='red', fg='black')

    def remove_tile(self):
        valueCopy = self.value.get()
        self.value.set(-1)
        self.tile.configure(bg='lightgrey', fg="lightgrey")
        return valueCopy


if __name__ == "__main__":
    game_board = GameBoard()
    game_board.mainloop()
