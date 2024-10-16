import sys
import chess
from minimax import find_best_move
import chess.polyglot

def print_board(board, color):
    if color == "b":
        print(board.transform(chess.flip_vertical))
    else:
        print(board)

def main():
    board = chess.Board()

    while True:
        try:
            depth = int(input("Depth (1-6): "))
            if 1 <= depth <= 6:
                break
            else:
                print("Please enter a depth between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        color = input("Color (w/b): ").lower()
        if color in ["w", "b"]:
            break
        else:
            print("Invalid input. Please enter 'w' for white or 'b' for black.")

    if color == "b":
        ai_move = find_best_move(board, depth)
        board.push(ai_move)
        print("AI move:" + str(ai_move))
        print_board(board, color)
        print("\n")

    while not board.is_game_over():
        while True:
            user_move = input("Your move (in UCI format): ").lower()
            try:
                board.push_uci(user_move)
                print_board(board, color)
                print("\n")
                break
            except ValueError:
                print("Invalid move. Please try again.")

        if board.is_game_over():
            break

        ai_move = find_best_move(board, depth)
        board.push(ai_move)
        print("AI move:" + str(ai_move))
        print_board(board, color)
        print("\n")

    print("Game over!")
    print(board.result())

if __name__ == "__main__":
    main()
