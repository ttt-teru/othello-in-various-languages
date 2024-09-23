import tkinter as tk
import tkinter.ttk as ttk

from algo import OthelloAlgorithm

class Othello():
    BOARD_SIZE = 500

    BOARD_COLOR = 'green'
    BORDER_COLOR = 'black'
    BLACK_COLOR = 'black'
    WHITE_COLOR = 'white'

    def __init__(self, frame):
        self.frame = frame
        self.frame.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

    def game(self):
        self.algo = OthelloAlgorithm()

        self.NUM_SQUARE = self.algo.BOARD_WIDTH if self.algo.BOARD_WIDTH >= self.algo.BOARD_HEIGHT else self.algo.BOARD_HEIGHT
        self.NUM_SQUARE_WIDTH = self.algo.BOARD_WIDTH
        self.NUM_SQUARE_HEIGHT = self.algo.BOARD_HEIGHT

        self.create_board()
        self.set_events()
        self.init_board()
        self.draw_discs()
        print("Game Start")
        print("Black")

    def set_events(self):
        self.board.bind('<ButtonPress>', self.click)

    def create_board(self):
        self.board = tk.Canvas(
            frame,
            # bg = self.BOARD_COLOR,
            width = self.BOARD_SIZE+1,
            height = self.BOARD_SIZE+1,
            highlightthickness = 0
        )
        self.board.pack(padx=10, pady=10)

    def init_board(self):
        self.square_size = self.BOARD_SIZE / self.NUM_SQUARE
        for y in range(self.NUM_SQUARE_HEIGHT):
            for x in range(self.NUM_SQUARE_WIDTH):
                xs = x * self.square_size
                ys = y * self.square_size
                xe = (x + 1) * self.square_size
                ye = (y + 1) * self.square_size

                self.board.create_rectangle(
                    xs, ys,
                    xe, ye,
                    fill = self.BOARD_COLOR,
                )

    def draw_discs(self):
        for y in range(self.NUM_SQUARE_HEIGHT):
            for x in range(self.NUM_SQUARE_WIDTH):
                if self.algo.board[y][x] != self.algo.NONE:
                    xs = x * self.square_size
                    ys = y * self.square_size
                    xe = (x + 1) * self.square_size
                    ye = (y + 1) * self.square_size

                    center_x = (x + 0.5) * self.square_size
                    center_y = (y + 0.5) * self.square_size

                    xs = center_x - (self.square_size * 0.9) / 2
                    ys = center_y - (self.square_size * 0.9) / 2
                    xe = center_x + (self.square_size * 0.9) / 2
                    ye = center_y + (self.square_size * 0.9) / 2

                    self.board.create_oval(
                        xs, ys,
                        xe, ye,
                        fill = self.BLACK_COLOR if self.algo.board[y][x] == 0 else self.WHITE_COLOR,
                    )

    def click(self, event):
        x = int(event.x // self.square_size)
        y = int(event.y // self.square_size)
        if square_list := self.algo.put_disc(x, y):
            # print(square_list)
            print("White" if self.algo.player == 1 else "Black")
            self.draw_discs()
        else:
            print("Not put.")

        if not self.algo.get_square_list():
            self.algo.player ^= 1
            if not self.algo.get_square_list():
                black_num, white_num = self.algo.get_disc_count()
                if black_num > white_num:
                    print(black_num, "Winner Black!!")
                elif black_num < white_num:
                    print(white_num, "Winner White!!")
                elif black_num == white_num:
                    print("Draw.")
            else:
                print("Black" if self.algo.player == 1 else "White", "pass")



if __name__ == '__main__':
    root = tk.Tk()
    root.title("Othello Game")
    root.geometry("600x600")

    frame = ttk.Frame(root)

    othello = Othello(frame)
    othello.game()

    root.mainloop()
