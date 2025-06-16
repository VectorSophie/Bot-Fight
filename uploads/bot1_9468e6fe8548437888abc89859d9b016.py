def make_move(board, symbol):
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                return (r, c)



