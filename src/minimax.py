import math
import chess
import concurrent.futures
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

history_table = {}


def update_history(move, depth):
    if move not in history_table:
        history_table[move] = 0
    history_table[move] += depth ** 2


def move_ordering(board, move):
    board.push(move)
    score = 0
    if board.is_checkmate():
        board.pop()
        return 10000
    board.pop()
    if board.gives_check(move):
        score += 10
    if board.is_capture(move):
        score += 5
    score += history_table.get(move, 0)
    return score


def transposition_key(board):
    return chess.polyglot.zobrist_hash(board)


def material_count(board):
    material = 0
    for piece_type in piece_values:
        material += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        material += len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
    return material


def minimax(board, depth, alpha, beta, is_maximizing):
    key = transposition_key(board)

    if key in transposition_table and transposition_table[key]['depth'] >= depth:
        entry = transposition_table[key]
        if entry['flag'] == 'exact':
            return entry['eval']
        elif entry['flag'] == 'lower':
            alpha = max(alpha, entry['eval'])
        elif entry['flag'] == 'upper':
            beta = min(beta, entry['eval'])
        if alpha >= beta:
            return entry['eval']

    if depth == 0 or board.is_game_over() or board.can_claim_threefold_repetition():
        score = evaluate(board, is_maximizing)
        transposition_table[key] = {'eval': score, 'depth': depth, 'flag': 'exact'}
        return score

    if is_maximizing:
        max_eval = float('-inf')
        for move in sorted(board.legal_moves, key=lambda move: move_ordering(board, move), reverse=True):
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return float('inf')
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        flag = 'exact' if alpha < beta else 'lower'
        transposition_table[key] = {'eval': max_eval, 'depth': depth, 'flag': flag}
        return max_eval
    else:
        min_eval = float('inf')
        for move in sorted(board.legal_moves, key=lambda move: move_ordering(board, move)):
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return -float('inf')
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        flag = 'exact' if alpha < beta else 'upper'
        transposition_table[key] = {'eval': min_eval, 'depth': depth, 'flag': flag}
        return min_eval


def get_moves_from_book(board, book_file):
    try:
        with chess.polyglot.open_reader(book_file) as reader:
            main_entry = reader.find(board)
            return main_entry.move if main_entry else None
    except (IOError, IndexError, ValueError):
        return None


def evaluate_move(board, move, original_depth, alpha, beta):
    board_copy = board.copy(stack=False)
    board_copy.push(move)
    eval = minimax(board_copy, original_depth - 1, alpha, beta, board_copy.turn)
    return move, eval


def find_best_move(board, original_depth):
    alpha = float("-inf")
    beta = float("inf")
    best_eval = -math.inf
    worst_eval = math.inf
    best_move = None
    depth = original_depth

    if abs(material_count(board)) < 23000:
        depth += 1

    book_move = get_moves_from_book(board, "performance.bin")
    if book_move is not None:
        return book_move

    moves = list(sorted(board.legal_moves, key=lambda move: move_ordering(board, move), reverse=True))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(evaluate_move, board, move, depth, alpha, beta) for move in moves]
        for future in concurrent.futures.as_completed(futures):
            move, eval = future.result()
            board.push(move)

            if board.is_checkmate():
                board.pop()
                return move

            repetition = 1 if (evaluate(board, True) > 0 and not board.turn or evaluate(board,
                                                                                        False) < 0 and board.turn) else 0
            skip = 1 if (board.is_fivefold_repetition() and repetition == 1) else 0
            board.pop()

            if skip == 0:
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
