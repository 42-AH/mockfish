import chess

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 9999
}

piece_square_tables = {
    chess.PAWN: [0,   0,   0,   0,   0,   0,   0,   0,
                0,   0,   0, -40, -40,   0,   0,   0,
                1,   2,   3, -10, -10,   3,   2,   1,
                2,   4,   6,   8,   8,   6,   4,   2,
                3,   6,   9,  12,  12,   9,   6,   3,
                4,   8,  12,  16,  16,  12,   8,   4,
                5,  10,  15,  20,  20,  15,  10,   5,
                0,   0,   0,   0,   0,   0,   0,   0],

    chess.KNIGHT: [-10, -10, -10, -10, -10, -10, -10, -10,
                    -10,   0,   0,   0,   0,   0,   0, -10,
                    -10,   0,   5,   5,   5,   5,   0, -10,
                    -10,   0,   5,  10,  10,   5,   0, -10,
                    -10,   0,   5,  10,  10,   5,   0, -10,
                    -10,   0,   5,   5,   5,   5,   0, -10,
                    -10,   0,   0,   0,   0,   0,   0, -10,
                    -10, -30, -10, -10, -10, -10, -30, -10],

    chess.BISHOP: [-10, -10, -10, -10, -10, -10, -10, -10,
                    -10,   0,   0,   0,   0,   0,   0, -10,
                    -10,   0,   5,   5,   5,   5,   0, -10,
                    -10,   0,   5,  10,  10,   5,   0, -10,
                    -10,   0,   5,  10,  10,   5,   0, -10,
                    -10,   0,   5,   5,   5,   5,   0, -10,
                    -10,   0,   0,   0,   0,   0,   0, -10,
                    -10, -10, -20, -10, -10, -20, -10, -10],

    chess.ROOK: [0, -75, 0, 100, 5, 100, -75, 0,
                 -5, 0, 0, 0, 0, 0, 0, -5,
                 -5, 0, 0, 0, 0, 0, 0, -5,
                 -5, 0, 0, 0, 0, 0, 0, -5,
                 -5, 0, 0, 0, 0, 0, 0, -5,
                 -5, 0, 0, 0, 0, 0, 0, -5,
                 5, 10, 10, 10, 10, 10, 10, 5,
                 0, 0, 0, 0, 0, 0, 0, 0],

    chess.QUEEN: [-20,-10,-10, -5, -5,-10,-10,-20,
                  -10,  0,  0,  0,  0,  0,  0,-10,
                  -10,  0,  5,  5,  5,  5,  0,-10,
                   -5,  0,  5,  5,  5,  5,  0, -5,
                    0,  0,  5,  5,  5,  5,  0, -5,
                  -10,  5,  5,  5,  5,  5,  0,-10,
                  -10,  0,  5,  0,  0,  0,  0,-10,
                  -20,-10,-10, -5, -5,-10,-10,-20],

    chess.KING: [0,  20,  100, -20,   0, -20,  100,  20,
                 -20, -20, -20, -20, -20, -20, -20, -20,
                 -40, -40, -40, -40, -40, -40, -40, -40,
                 -40, -40, -40, -40, -40, -40, -40, -40,
                 -40, -40, -40, -40, -40, -40, -40, -40,
                 -40, -40, -40, -40, -40, -40, -40, -40,
                 -40, -40, -40, -40, -40, -40, -40, -40,
                 -40, -40, -40, -40, -40, -40, -40, -40]
}

king_endgame = [0, 10, 20, 30, 30, 20, 10, 0,
                10, 20, 30, 40, 40, 30, 20, 10,
                20, 30, 40, 50, 50, 40, 30, 20,
                30, 40, 50, 60, 60, 50, 40, 30,
                30, 40, 50, 60, 60, 50, 40, 30,
                20, 30, 40, 50, 50, 40, 30, 20,
                10, 20, 30, 40, 40, 30, 20, 10,
                0, 10, 20, 30, 30, 20, 10, 0]

rook_endgame = [0, 0, 0, 5, 5, 0, 0, 0,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                5, 10, 10, 10, 10, 10, 10, 5,
                0, 0, 0, 0, 0, 0, 0, 0]



def evaluate(board, maximizing):
    player_color = chess.WHITE if board.turn else chess.BLACK
    opponent_color = not player_color

    if board.is_checkmate():
        return 9999 if board.turn == chess.BLACK else -9999
    if board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition():
        return 0

    material = sum(
        (len(board.pieces(piece, player_color)) - len(board.pieces(piece, opponent_color))) * value
        for piece, value in piece_values.items()
    )

    total = sum(
        (len(board.pieces(piece, player_color)) + len(board.pieces(piece, opponent_color))) * value
        for piece, value in piece_values.items()
    )

    if total < 23000:
        piece_square_tables[chess.KING] = king_endgame
        piece_square_tables[chess.ROOK] = rook_endgame

    piece_square_eval = 0
    for piece in piece_square_tables:
        piece_squares = board.pieces(piece, player_color)
        opponent_piece_squares = board.pieces(piece, opponent_color)
        if player_color == chess.WHITE:
            piece_square_eval += sum(piece_square_tables[piece][chess.square_mirror(square)] for square in piece_squares)
            piece_square_eval -= sum(piece_square_tables[piece][square] for square in opponent_piece_squares)
        else:
            piece_square_eval += sum(piece_square_tables[piece][square] for square in piece_squares)
            piece_square_eval -= sum(piece_square_tables[piece][chess.square_mirror(square)] for square in opponent_piece_squares)

    total_evaluation = material + piece_square_eval

    doubled_penalty = 30
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_square = piece_square_tables.get(piece.piece_type, [0]*64)
            if piece.piece_type == chess.PAWN:
                if square + 8 < 64 and board.piece_at(square + 8) == piece:
                    total_evaluation -= doubled_penalty
                if square - 8 >= 0 and board.piece_at(square - 8) == piece:
                    total_evaluation -= doubled_penalty
    return total_evaluation if maximizing else -total_evaluation
