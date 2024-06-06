import chess


def get_square(row, column):
    return chess.square(column, 7 - row)


def evaluate(board, maximizing):
    player_color = chess.WHITE if board.turn else chess.BLACK
    opponent_color = not player_color

    if board.is_checkmate():
        outcome = board.outcome()
        if outcome:
            return -9999 if board.turn else 9999
    if board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition() or board.can_claim_threefold_repetition():
        return 0

    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 9999
    }

    material = sum(
        (len(board.pieces(piece, player_color)) - len(board.pieces(piece, opponent_color))) * value for piece, value in
        piece_values.items())

    total = sum(
        (len(board.pieces(piece, player_color)) + len(board.pieces(piece, opponent_color))) * value for piece, value in
        piece_values.items())

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

        chess.ROOK: [0, -75, 0, 5, 5, 0, -75, 0,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     -5, 0, 0, 0, 0, 0, 0, -5,
                     5, 10, 10, 10, 10, 10, 10, 5,
                     0, 0, 0, 0, 0, 0, 0, 0, ],

        chess.QUEEN: [-20,-10,-10, -5, -5,-10,-10,-20,
                        -10,  0,  0,  0,  0,  0,  0,-10,
                        -10,  0,  5,  5,  5,  5,  0,-10,
                         -5,  0,  5,  5,  5,  5,  0, -5,
                          0,  0,  5,  5,  5,  5,  0, -5,
                        -10,  5,  5,  5,  5,  5,  0,-10,
                        -10,  0,  5,  0,  0,  0,  0,-10,
                        -20,-10,-10, -5, -5,-10,-10,-20],

        chess.KING: [  0,  20,  40, -20,   0, -20,  40,  20,
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
                     0, 0, 0, 0, 0, 0, 0, 0, ]

    if total < 2000:
        piece_square_tables[chess.KING] = king_endgame
        piece_square_tables[chess.ROOK] = rook_endgame
    if player_color == chess.WHITE:
        piece_square_eval = sum(piece_square_tables[piece][square] for piece in piece_square_tables for square in
                                board.pieces(piece, player_color))
        piece_square_eval -= sum(
            piece_square_tables[piece][chess.square_mirror(square)] for piece in piece_square_tables for square in
            board.pieces(piece, opponent_color))
    else:
        piece_square_eval = sum(
            piece_square_tables[piece][chess.square_mirror(square)] for piece in piece_square_tables for square in
            board.pieces(piece, player_color))
        piece_square_eval -= sum(piece_square_tables[piece][square] for piece in piece_square_tables for square in
                                 board.pieces(piece, opponent_color))
    total_evaluation = material + piece_square_eval

    doubled_penalty = 30
    for row in range(8):
        for column in range(8):
            square = get_square(row, column)
            piece = board.piece_at(square)

            if piece and piece.symbol() == "P":
                if row + 1 < 8:
                    piece_above = board.piece_at(get_square(row + 1, column))
                    if piece_above and piece_above.symbol() == "P":
                        total_evaluation -= doubled_penalty
                if row - 1 >= 0:
                    piece_below = board.piece_at(get_square(row - 1, column))
                    if piece_below and piece_below.symbol() == "P":
                        total_evaluation -= doubled_penalty
            elif piece and piece.symbol() == "p":
                if row + 1 < 8:
                    piece_above = board.piece_at(get_square(row + 1, column))
                    if piece_above and piece_above.symbol() == "p":
                        total_evaluation += doubled_penalty
                if row - 1 >= 0:
                    piece_below = board.piece_at(get_square(row - 1, column))
                    if piece_below and piece_below.symbol() == "p":
                        total_evaluation += doubled_penalty

    return total_evaluation if maximizing else -total_evaluation
