import math
import chess
import concurrent.futures
import copy
import chess.polyglot
from eval import evaluate

board = chess.Board()

transposition_table = {}

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 9999
}


def move_ordering(board, move):
    board.push(move)
    if board.is_checkmate():
        board.pop()
        return 20
    board.pop()
    if board.gives_check(move):
        return 10
    if board.is_capture(move):
        return 5
    return 0


def transposition_key(board):
    return board.fen()


def material_count(board):
    material = 0
    for piece_type in piece_values:
        material += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        material += len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    return material


def minimax(board, depth, alpha, beta, is_maximizing):
    key = transposition_key(board)
    if key in transposition_table:
        entry = transposition_table[key]
        if entry['depth'] >= depth:
            return entry['eval']

    if depth == 0 or board.is_game_over():
        score = evaluate(board, is_maximizing)
        transposition_table[key] = {'eval': score, 'depth': depth}
        return score

    if is_maximizing:
        max_eval = float('-inf')
        for move in sorted(board.legal_moves, key=lambda move: move_ordering(board, move), reverse=True):
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        transposition_table[key] = {'eval': max_eval, 'depth': depth}
        return max_eval
    else:
        min_eval = float('inf')
        for move in sorted(board.legal_moves, key=lambda move: move_ordering(board, move)):
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        transposition_table[key] = {'eval': min_eval, 'depth': depth}
        return min_eval


def get_moves_from_book(board, book_file):
    try:
        with chess.polyglot.open_reader(book_file) as reader:
            main_entry = reader.find(board)
            if main_entry:
                return main_entry.move
            else:
                return None
    except (IOError, IndexError, ValueError) as e:
        return None


def evaluate_move(board, move, original_depth, alpha, beta):
    board_copy = copy.deepcopy(board)
    board_copy.push(move)
    eval = minimax(board_copy, original_depth - 1, alpha, beta, board_copy.turn)
    return (move, eval)


def find_best_move(board, original_depth):
    alpha = float("-inf")
    beta = float("inf")
    best_eval = -math.inf
    worst_eval = math.inf
    best_move = None
    depth = original_depth
    if abs(material_count(board)) < 23000:
        depth += 1
    print(material_count(board))
    book = get_moves_from_book(board, "performance.bin")
    if book is not None:
        return book
    moves = list(sorted(board.legal_moves, key=lambda move: move_ordering(board, move), reverse=True))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(evaluate_move, board, move, depth, alpha, beta) for move in moves]
        for future in concurrent.futures.as_completed(futures):
            move, eval = future.result()
            if board.turn:
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
            else:
                if eval < worst_eval:
                    worst_eval = eval
                    best_move = move
                beta = min(beta, eval)
            if beta <= alpha:
                break

    return best_move
