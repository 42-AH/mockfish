import math

import chess

from eval import evaluate

board = chess.Board()


def minimax(board, depth, is_maximizing):
  score = evaluate(board, is_maximizing) 
  if depth == 0:
      return score
  if is_maximizing:
      max_eval = float('-inf')
      for move in board.legal_moves:
          board.push(move)
          eval = minimax(board, depth - 1, False)
          board.pop()
          max_eval = max(max_eval, eval)
      return max_eval
  else:
      min_eval = float('inf')
      for move in board.legal_moves:
          board.push(move)
          eval = minimax(board, depth - 1, True)
          board.pop()
          min_eval = min(min_eval, eval)
      return min_eval
def find_best_move(board, original_depth):
    best_eval = -math.inf
    best_move = None
    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, original_depth, not board.turn)
        board.pop()
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move
