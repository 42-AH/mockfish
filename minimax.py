import math

import chess

from eval import evaluate

board = chess.Board()


def minimax(board, depth, alpha, beta, is_maximizing):
  if depth == 0 or board.is_game_over():
      score = evaluate(board, board.turn) 
      return score
  if is_maximizing:
      max_eval = float('-inf')
      for move in board.legal_moves:
          board.push(move)
          eval = minimax(board, depth - 1, alpha, beta, False)
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
          eval = minimax(board, depth - 1, alpha, beta, True)
          board.pop()
          min_eval = min(min_eval, eval)
          beta = min(beta, eval)
          if beta <= alpha:
              break
      return min_eval
def find_best_move(board, original_depth):
  alpha = float("-inf")
  beta = float("inf")
  best_eval = -math.inf
  best_move = None
  for move in board.legal_moves:
      board.push(move)
      eval = minimax(board, original_depth, alpha, beta, False)
      board.pop()
      if eval > best_eval:
          best_eval = eval
          best_move = move
      alpha = max(alpha, eval)
  return best_move
