import chess
from chess_ai import ChessAI

unicode_pieces = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚',
    '.': '⭘'
}

def print_unicode_board(board):
    board_str = board.board_fen()
    rows = board_str.split('/')
    print()
    for row in rows:
        line = ''
        for ch in row:
            if ch.isdigit():
                line += ' '.join([unicode_pieces['.']] * int(ch)) + ' '
            else:
                line += unicode_pieces[ch] + ' '
        print(line.strip())
    print()

def play():
    board = chess.Board()
    ai = ChessAI(depth=3)

    move_count = 1
    print("Starting Game:\n")

    while not board.is_game_over():
        print(f"Move {move_count}")
        print_unicode_board(board)

        move = ai.get_best_move(board)
        color = 'White' if board.turn else 'Black'
        print(f"{color} plays: {move}\n")

        board.push(move)
        move_count += 1

    print("Final Position:")
    print_unicode_board(board)
    print("Result:", board.result())

    outcome = board.outcome()
    if outcome.winner is None:
        print("🏳️ Game ended in a draw!")
    elif outcome.winner:
        print("🏁 White wins!")
    else:
        print("🏁 Black wins!")

    print("\nGame Over Reason:", outcome)

if __name__ == "__main__":
    play()