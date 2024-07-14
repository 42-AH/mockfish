import tkinter as tk
from PIL import Image, ImageTk
import os
import chess
from minimax import find_best_move
import sys


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


class ChessUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MOCKFISH by 42-AH")

        self.depth = tk.IntVar(value=1)
        self.color = tk.StringVar(value="WHITE")

        self.create_controls()
        self.canvas = tk.Canvas(master, width=800, height=800)
        self.canvas.pack()
        self.board = chess.Board()
        self.selected_square = None
        self.load_pieces()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        self.master.configure(bg="#D2B48C")
    def start_game(self):
        self.board.reset()
        self.draw_board()
        if self.color.get() == "BLACK":
            self.bot_move()

    def create_controls(self):
        control_frame = tk.Frame(self.master, bg="#D2B48C")
        control_frame.pack()
        start_game_button = tk.Button(control_frame, text="Start Game", command=self.start_game, bg="#D2B48C")
        start_game_button.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        tk.Label(control_frame, text="Difficulty:", bg="#D2B48C").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Easy", variable=self.depth, value=1, bg="#D2B48C").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Medium", variable=self.depth, value=2, bg="#D2B48C").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Hard", variable=self.depth, value=3, bg="#D2B48C").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Extreme", variable=self.depth, value=4, bg="#D2B48C").pack(side=tk.LEFT)
        tk.Label(control_frame, text="                               ", bg="#D2B48C").pack(side=tk.LEFT)
        tk.Label(control_frame, text="Player Color:", bg="#D2B48C").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="    ", variable=self.color, value="BLACK", bg="black").pack(side=tk.BOTTOM)
        tk.Radiobutton(control_frame, text="    ", variable=self.color, value="WHITE", bg="white").pack(side=tk.BOTTOM)

    def on_square_clicked(self, event):
        col = event.x // 100
        row = 7 - (event.y // 100)
        square = chess.square(col, row)

        piece = self.board.piece_at(square)
        if piece is not None and ((piece.color == chess.WHITE and self.board.turn) or \
                                  (piece.color == chess.BLACK and not self.board.turn)):
            self.selected_square = square
        elif self.selected_square is not None:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.place_piece(move)
                self.selected_square = None

    def load_pieces(self):
        self.piece_images = {}
        assets_path = resource_path("assets")
        for filename in os.listdir(assets_path):
            if filename.endswith(".ico"):
                name = filename.split(".")[0]
                image = Image.open(os.path.join(assets_path, filename))
                image = image.resize((100, 100))
                self.piece_images[name] = ImageTk.PhotoImage(image)

    def draw_board(self):
        self.canvas.delete("pieces")
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(col * 100, row * 100, (col + 1) * 100, (row + 1) * 100, fill=color)
                piece = self.board.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_name = self.get_piece_name(piece)
                    self.canvas.create_image(col * 100 + 50, row * 100 + 50, image=self.piece_images[piece_name],
                                             tags="pieces")

    def get_piece_name(self, piece):
        piece_map = {
            chess.PAWN: "P",
            chess.KNIGHT: "N",
            chess.BISHOP: "B",
            chess.ROOK: "R",
            chess.QUEEN: "Q",
            chess.KING: "K"
        }
        color = "w" if piece.color == chess.WHITE else "b"
        return color + piece_map[piece.piece_type]

    def place_piece(self, move):
        self.board.push(move)
        self.draw_board()
        self.master.update()
        if self.board.is_game_over():
            self.game_over_message()
        else:
            self.bot_move()

    def bot_move(self):
        bot_move = find_best_move(self.board, self.depth.get())
        self.board.push(bot_move)
        self.draw_board()
        if self.board.is_game_over():
            self.game_over_message()

    def game_over_message(self):
        if self.board.is_checkmate():
            if self.board.turn:
                print("Black won")
            else:
                print("White won")
        elif self.board.is_stalemate():
            print("Draw")
        elif self.board.is_insufficient_material():
            print("Insufficient material")
        elif self.board.is_fivefold_repetition():
            print("Fivefold repetition")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChessUI(root)
    root.mainloop()