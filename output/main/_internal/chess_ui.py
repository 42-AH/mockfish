import tkinter as tk
from PIL import Image, ImageTk
import os
import chess
from minimax import find_best_move
import sys


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)

class ChessUI:
    def __init__(self, master, depth, player_color):
        self.master = master
        self.master.title("Chess UI")
        self.canvas = tk.Canvas(master, width=800, height=800)
        self.canvas.pack()

        self.board = chess.Board()
        self.selected_square = None
        self.load_pieces()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        self.depth = depth
        self.color = player_color
        if self.color == "BLACK":
            self.bot_move()

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
        bot_move = find_best_move(self.board, self.depth)
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