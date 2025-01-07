import chess
from functools import lru_cache

piece_square_tables = {
    chess.PAWN: [
        0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0,
    ],
    chess.KNIGHT: [
        -167, -89, -34, -49, 61, -97, -15, -107,
        -73, -41, 72, 36, 23, 62, 7, -17,
        -47, 60, 37, 65, 84, 129, 73, 44,
        -9, 17, 19, 53, 37, 69, 18, 22,
        -13, 4, 16, 13, 28, 19, 21, -8,
        -23, -9, 12, 10, 19, 17, 25, -16,
        -29, -53, -12, -3, -1, 18, -14, -19,
        -105, -21, -58, -33, -17, -28, -19, -23
    ],
    chess.BISHOP: [
        -29, 4, -82, -37, -25, -42, 7, -8,
        -26, 16, -18, -13, 30, 59, 18, -47,
        -16, 37, 43, 40, 35, 50, 37, -2,
        -4, 5, 19, 50, 37, 37, 7, -2,
        -6, 13, 13, 26, 34, 12, 10, 4,
        0, 15, 15, 15, 14, 27, 18, 10,
        4, 15, 16, 0, 7, 21, 33, 1,
        -33, -3, -14, -21, -13, -12, -39, -21
    ],
    chess.ROOK: [
        32, 42, 32, 51, 63, 9, 31, 43,
        27, 32, 58, 62, 80, 67, 26, 44,
        -5, 19, 26, 36, 17, 45, 61, 16,
        -24, -11, 7, 26, 24, 35, -8, -20,
        -36, -26, -12, -1, 9, -7, 6, -23,
        -45, -25, -16, -17, 3, 0, -5, -33,
        -44, -16, -20, -9, -1, 11, -6, -71,
        -19, -13, 1, 17, 16, 7, -37, -26
    ],
    chess.QUEEN: [
        -28, 0, 29, 12, 59, 44, 43, 45,
        -24, -39, -5, 1, -16, 57, 28, 54,
        -13, -17, 7, 8, 29, 56, 47, 57,
        -27, -27, -16, -16, -1, 17, -2, 1,
        -9, -26, -9, -10, -2, -4, 3, -3,
        -14, 2, -11, -2, -5, 2, 14, 5,
        -35, -8, 11, 2, 8, 15, -3, 1,
        -1, -18, -9, 10, -15, -25, -31, -50
    ],
    chess.KING: [
        -65, 23, 16, -15, -56, -34, 2, 13,
        29, -1, -20, -7, -8, -4, -38, -29,
        -9, 24, 2, -16, -20, 6, 22, -22,
        -17, -20, -12, -27, -30, -25, -14, -36,
        -49, -1, -27, -39, -46, -44, -33, -51,
        -14, -14, -22, -46, -44, -30, -15, -27,
        1, 7, -8, -64, -43, -16, 9, 8,
        -15, 36, 12, -54, 8, -28, 24, 14
    ]
}

@lru_cache(maxsize=10000)
def evaluate(board, maximizing):
    piece_values = {
        chess.PAWN: 82,
        chess.KNIGHT: 337,
        chess.BISHOP: 365,
        chess.ROOK: 477,
        chess.QUEEN: 1025,
        chess.KING: 0
    }

    player_color = chess.WHITE if board.turn else chess.BLACK
    opponent_color = not player_color

    if board.is_checkmate():
        return 9999 if board.turn == chess.BLACK else -9999
    if board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition() or board.can_claim_threefold_repetition():
        return 0

    player_pieces = {piece: list(board.pieces(piece, player_color)) for piece in piece_values}
    opponent_pieces = {piece: list(board.pieces(piece, opponent_color)) for piece in piece_values}

    material = sum(
        (len(player_pieces[piece]) - len(opponent_pieces[piece])) * value
        for piece, value in piece_values.items()
    )

    piece_square_eval = 0
    for piece in piece_square_tables:
        piece_squares = player_pieces[piece]
        opponent_piece_squares = opponent_pieces[piece]
        if player_color == chess.WHITE:
            piece_square_eval += sum(
                piece_square_tables[piece][chess.square_mirror(square)] for square in piece_squares)
            piece_square_eval -= sum(piece_square_tables[piece][square] for square in opponent_piece_squares)
        else:
            piece_square_eval += sum(piece_square_tables[piece][square] for square in piece_squares)
            piece_square_eval -= sum(
                piece_square_tables[piece][chess.square_mirror(square)] for square in opponent_piece_squares)

    total_evaluation = material + piece_square_eval

    doubled_penalty = 30
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.PAWN:
            if square + 8 < 64 and board.piece_at(square + 8) == piece:
                total_evaluation -= doubled_penalty
            if square - 8 >= 0 and board.piece_at(square - 8) == piece:
                total_evaluation -= doubled_penalty

    return total_evaluation if maximizing else -total_evaluation
