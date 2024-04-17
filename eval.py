import chess

def evaluate(board, maximizing):
    if board.is_checkmate():
        return 9999 if not maximizing else -9999
    if board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition():
        return 0

    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900
    }

    player_color = chess.WHITE if board.turn else chess.BLACK
    opponent_color = not player_color

    material = sum((len(board.pieces(piece, player_color)) - len(board.pieces(piece, opponent_color))) * value for piece, value in piece_values.items())

    piece_square_tables = {
        chess.PAWN: [100, 100, 100, 100, 100, 100, 100, 100,
                     50,  50,  50,  50,  50,  50,  50,  50,
                     10,  10,  20,  30,  30,  20,  10,  10,
                     5,   5,   10,  25,  25,  10,  5,   5,
                     0,   0,   0,   20,  20,  0,   0,   0,
                     5,  -5,  -10,  0,   0,  -10, -5,   5,
                     5,  10,  10, -20, -20,  10,  10,  5,
                     0,   0,   0,   0,   0,   0,   0,   0],

        chess.KNIGHT: [-50, -40, -30, -30, -30, -30, -40, -50,
                        -40, -20,   0,   0,   0,   0, -20, -40,
                        -30,   0,  10,  15,  15,  10,   0, -30,
                        -30,   5,  15,  20,  20,  15,   5, -30,
                        -30,   0,  15,  20,  20,  15,   0, -30,
                        -30,   5,  10,  15,  15,  10,   5, -30,
                        -40, -20,   0,   5,   5,   0, -20, -40,
                        -50, -40, -20, -30, -30, -20, -40, -50],

        chess.BISHOP: [-20, -10, -10, -10, -10, -10, -10, -20,
                        -10,   0,   0,   0,   0,   0,   0, -10,
                        -10,   0,   5,  10,  10,   5,   0, -10,
                        -10,   5,   5,  10,  10,   5,   5, -10,
                        -10,   0,  10,  10,  10,  10,   0, -10,
                        -10,  10,  10,  10,  10,  10,  10, -10,
                        -10,   5,   0,   0,   0,   0,   5, -10,
                        -20, -10, -40, -10, -10, -40, -10, -20],

        chess.ROOK: [0, 0, 0, 0, 0, 0, 0, 0,
                     5, 10, 10, 10, 10, 10, 10, 5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     0, 0, 0, 5, 5, 0, 0, 0],

        chess.QUEEN: [-20, -10, -10, -5, -5, -10, -10, -20,
                        -10,   0,   0,  0,  0,  0,  0, -10,
                        -10,   0,   5,  5,  5,  5,  0, -10,
                        -5,   0,   5,  5,  5,  5,  0,  -5,
                         0,   0,   5,  5,  5,  5,  0,  -5,
                        -10,   5,   5,  5,  5,  5,  0, -10,
                        -10,   0,   5,  0,  0,  0,  0, -10,
                        -20, -10, -10, -5, -5, -10, -10, -20],

        chess.KING: [-30, -40, -40, -50, -50, -40, -40, -30,
                      -30, -40, -40, -50, -50, -40, -40, -30,
                      -30, -40, -40, -50, -50, -40, -40, -30,
                      -30, -40, -40, -50, -50, -40, -40, -30,
                      -20, -30, -30, -40, -40, -30, -30, -20,
                      -10, -20, -20, -20, -20, -20, -20, -10,
                       20,  20,   0,   0,   0,   0,  20,  20,
                       20,  30,  10,   0,   0,  10,  30,  20]
    }

    if player_color == chess.BLACK:
      for piece in piece_square_tables:
        piece_square_tables[piece] = piece_square_tables[piece][::-1]
    piece_square_eval = sum(piece_square_tables[piece][square] for piece in piece_square_tables for square in board.pieces(piece, player_color))
    piece_square_eval -= sum(piece_square_tables[piece][chess.square_mirror(square)] for piece in piece_square_tables for square in board.pieces(piece, opponent_color))

    total_evaluation = material + piece_square_eval

    return total_evaluation if maximizing else -total_evaluation

