import math
import chess
from eval import evaluate
import concurrent.futures
import copy

board = chess.Board()

def move_ordering(board, move):
    if board.gives_check(move):
        return 10
    if board.is_capture(move):
        return 5
    return 0

def minimax(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        score = evaluate(board, board.turn)
        if score == 9999 or score == -9999:
            score = score * (depth + 1)
        return score

    if is_maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, board.turn)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, board.turn)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

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

    moves = list(sorted(board.legal_moves, key=lambda move: move_ordering(board, move), reverse=True))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(evaluate_move, board, move, original_depth, alpha, beta) for move in moves]
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
