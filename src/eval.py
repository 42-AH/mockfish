import chess

def evaluate(board, maximizing):
      player_color = chess.WHITE if board.turn else chess.BLACK
      opponent_color = not player_color

      if board.is_checkmate():
        outcome = board.outcome()
        if outcome:
          return -9999 if board.turn else 9999
      if board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition():
          return 0

      piece_values = {
          chess.PAWN: 100,
          chess.KNIGHT: 320,
          chess.BISHOP: 330,
          chess.ROOK: 500,
          chess.QUEEN: 900
      }


      material = sum((len(board.pieces(piece, player_color)) - len(board.pieces(piece, opponent_color))) * value for piece, value in piece_values.items())

      piece_square_tables = {
          chess.PAWN: [0,  0,  0,  0,  0,  0,  0,  0,
                      5, 10, 10,-20,-20, 10, 10,  5,
                      5, -5,-10,  0,  0,-10, -5,  5,
                      0,  0,  0, 20, 20,  0,  0,  0,
                      5,  5, 10, 25, 25, 10,  5,  5,
                      10, 10, 20, 30, 30, 20, 10, 10,
                      50, 50, 50, 50, 50, 50, 50, 50,
                      0,  0,  0,  0,  0,  0,  0,  0],

          chess.KNIGHT: [-50,-40,-30,-30,-30,-30,-40,-50,
                        -40,-20,  0,  5,  5,  0,-20,-40,
                        -30,  5, 10, 15, 15, 10,  5,-30,
                        -30,  0, 15, 20, 20, 15,  0,-30,
                        -30,  5, 15, 20, 20, 15,  5,-30,
                        -30,  0, 10, 15, 15, 10,  0,-30,
                        -40,-20,  0,  0,  0,  0,-20,-40,
                        -50,-40,-30,-30,-30,-30,-40,-50],

          chess.BISHOP: [-20,-10,-10,-10,-10,-10,-10,-20,
                        -10,  5,  0,  0,  0,  0,  5,-10,
                        -10, 10, 10, 10, 10, 10, 10,-10,
                        -10,  0, 10, 10, 10, 10,  0,-10,
                        -10,  5,  5, 10, 10,  5,  5,-10,
                        -10,  0,  5, 10, 10,  5,  0,-10,
                        -10,  0,  0,  0,  0,  0,  0,-10,
                        -20,-10,-10,-10,-10,-10,-10,-20],

          chess.ROOK: [0,  0,  0,  5,  5,  0,  0,  0,
                       -5,  0,  0,  0,  0,  0,  0, -5,
                       -5,  0,  0,  0,  0,  0,  0, -5,
                       -5,  0,  0,  0,  0,  0,  0, -5,
                       -5,  0,  0,  0,  0,  0,  0, -5,
                       -5,  0,  0,  0,  0,  0,  0, -5,
                        5, 10, 10, 10, 10, 10, 10,  5,
                        0,  0,  0,  0,  0,  0,  0,  0,],

          chess.QUEEN: [6,   1,  -8,-104,  69,  24,  88,  26,
                         14,  32,  60, -10,  20,  76,  57,  24,
                         -2,  43,  32,  60,  72,  63,  43,   2,
                          1, -16,  22,  17,  25,  20, -13,  -6,
                        -14, -15,  -2,  -5,  -1, -10, -20, -22,
                        -30,  -6, -13, -11, -16, -11, -16, -27,
                        -36, -18,   0, -19, -15, -15, -21, -38,
                        -39, -30, -31, -13, -31, -36, -34, -42],

          chess.KING: [-20,-10,-10, -5, -5,-10,-10,-20,
                      -10,  0,  0,  0,  0,  0,  0,-10,
                      -10,  0,  5,  5,  5,  5,  0,-10,
                       -5,  0,  5,  5,  5,  5,  0, -5,
                        0,  0,  5,  5,  5,  5,  0, -5,
                      -10,  5,  5,  5,  5,  5,  0,-10,
                      -10,  0,  5,  0,  0,  0,  0,-10,
                      -20,-10,-10, -5, -5,-10,-10,-20]
      }

      if player_color == chess.WHITE:
          piece_square_eval = sum(piece_square_tables[piece][square] for piece in piece_square_tables for square in board.pieces(piece, player_color))
          piece_square_eval -= sum(piece_square_tables[piece][chess.square_mirror(square)] for piece in piece_square_tables for square in board.pieces(piece, opponent_color))
      else:
          piece_square_eval = sum(piece_square_tables[piece][chess.square_mirror(square)] for piece in piece_square_tables for square in board.pieces(piece, player_color))
          piece_square_eval -= sum(piece_square_tables[piece][square] for piece in piece_square_tables for square in board.pieces(piece, opponent_color))
      total_evaluation = material + piece_square_eval

      return total_evaluation if maximizing else -total_evaluation