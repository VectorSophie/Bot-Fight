import importlib.util
import time
import copy
import json
import uuid
import os

TIME_LIMIT = 1.0  # seconds

def load_bot(path):
    spec = importlib.util.spec_from_file_location("bot", path)
    bot = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot)
    return bot.make_move

def is_valid(board, move):
    r, c = move
    return 0 <= r < 3 and 0 <= c < 3 and board[r][c] == ""

def winner(board):
    lines = board + list(map(list, zip(*board))) + [
        [board[i][i] for i in range(3)],
        [board[i][2 - i] for i in range(3)],
    ]
    for line in lines:
        if line == ["X"] * 3: return "X"
        if line == ["O"] * 3: return "O"
    if all(cell for row in board for cell in row): return "draw"
    return None

def run_match(path1, path2):
    botX = load_bot(path1)
    botO = load_bot(path2)
    bots = [("X", botX), ("O", botO)]

    board = [["" for _ in range(3)] for _ in range(3)]
    history = []

    turn = 0
    while True:
        symbol, bot = bots[turn % 2]
        try:
            move = bot(copy.deepcopy(board), symbol)
        except Exception as e:
            return {"result": f"Bot {symbol} crashed", "history": history}
        
        if not is_valid(board, move):
            return {"result": f"Invalid move by {symbol}: {move}", "history": history}
        
        board[move[0]][move[1]] = symbol
        history.append({"turn": symbol, "move": move, "board": copy.deepcopy(board)})
        result = winner(board)
        if result:
            return {"result": result, "history": history}
        
        turn += 1
