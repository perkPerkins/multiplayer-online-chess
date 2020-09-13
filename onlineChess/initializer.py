from piece import Piece


def initialize_board(board, pieces):
    board[0][0].piece = Piece(pieces[7], "rook", "black")
    board[1][0].piece = Piece(pieces[8], "knight", "black")
    board[2][0].piece = Piece(pieces[9], "bishop", "black")
    board[3][0].piece = Piece(pieces[10], "queen", "black")
    board[4][0].piece = Piece(pieces[11], "king", "black")
    board[5][0].piece = Piece(pieces[9], "bishop", "black")
    board[6][0].piece = Piece(pieces[8], "knight", "black")
    board[7][0].piece = Piece(pieces[7], "rook", "black")

    board[0][1].piece = Piece(pieces[6], "pawn", "black")
    board[1][1].piece = Piece(pieces[6], "pawn", "black")
    board[2][1].piece = Piece(pieces[6], "pawn", "black")
    board[3][1].piece = Piece(pieces[6], "pawn", "black")
    board[4][1].piece = Piece(pieces[6], "pawn", "black")
    board[5][1].piece = Piece(pieces[6], "pawn", "black")
    board[6][1].piece = Piece(pieces[6], "pawn", "black")
    board[7][1].piece = Piece(pieces[6], "pawn", "black")

    board[0][7].piece = Piece(pieces[1], "rook", "white")
    board[1][7].piece = Piece(pieces[2], "knight", "white")
    board[2][7].piece = Piece(pieces[3], "bishop", "white")
    board[3][7].piece = Piece(pieces[4], "queen", "white")
    board[4][7].piece = Piece(pieces[5], "king", "white")
    board[5][7].piece = Piece(pieces[3], "bishop", "white")
    board[6][7].piece = Piece(pieces[2], "knight", "white")
    board[7][7].piece = Piece(pieces[1], "rook", "white")

    board[0][6].piece = Piece(pieces[0], "pawn", "white")
    board[1][6].piece = Piece(pieces[0], "pawn", "white")
    board[2][6].piece = Piece(pieces[0], "pawn", "white")
    board[3][6].piece = Piece(pieces[0], "pawn", "white")
    board[4][6].piece = Piece(pieces[0], "pawn", "white")
    board[5][6].piece = Piece(pieces[0], "pawn", "white")
    board[6][6].piece = Piece(pieces[0], "pawn", "white")
    board[7][6].piece = Piece(pieces[0], "pawn", "white")
    return board, pieces
