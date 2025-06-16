import random
def make_move(board, symbol):
    moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
    return random.choice(moves)
