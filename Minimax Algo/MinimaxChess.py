import chess
import random
import numpy as np
from gym import spaces
import gym

class ChessEnv(gym.Env):
    def __init__(self):
        self.board = chess.Board()
        self.action_space = spaces.Discrete(4672)
        self.observation_space = spaces.Discrete(64 * 8)

    def reset(self):
        self.board = chess.Board()
        return self.render()

    def step(self, action):
        legal_moves = list(self.board.legal_moves)
        if action < len(legal_moves):
            move = legal_moves[action]
            self.board.push(move)
            
            if self.board.is_checkmate():
                reward = 1000
            elif self.board.is_stalemate() or self.board.is_insufficient_material():
                reward = -100
            else:
                reward = 0
            
            done = self.board.is_game_over()
            return self.render(), reward, done, {}
        else:
            return self.render(), -1, False, {}

    def render(self, mode='human'):
        piece_unicode = {
            chess.PAWN: '♙', chess.KNIGHT: '♘', chess.BISHOP: '♗', chess.ROOK: '♖',
            chess.QUEEN: '♕', chess.KING: '♔',
            -chess.PAWN: '♟', -chess.KNIGHT: '♞', -chess.BISHOP: '♝', -chess.ROOK: '♜',
            -chess.QUEEN: '♛', -chess.KING: '♚'
        }
        board_str = ''
        for row in range(7, -1, -1):
            for col in range(8):
                piece = self.board.piece_at(chess.square(col, row))
                if piece is None:
                    board_str += '⭘ '
                else:
                    if piece.color == chess.WHITE:
                        board_str += f'\033[1m{piece_unicode[piece.piece_type]}\033[0m '
                    else:
                        board_str += f'{piece_unicode[-piece.piece_type]} '
            board_str += '\n'
        print(board_str)
        return board_str
    

def evaluate_board(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -1000
        else:
            return 1000

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_value = piece_values.get(piece.piece_type, 0)
            if piece.color == chess.WHITE:
                score += piece_value
            else:
                score -= piece_value

    central_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
    for square in central_squares:
        piece = board.piece_at(square)
        if piece is not None and piece.piece_type == chess.PAWN:
            if piece.color == chess.WHITE:
                score += 0.5
            else:
                score -= 0.5

    if len(list(board.pieces(chess.QUEEN, chess.WHITE))) == 0 and len(list(board.pieces(chess.QUEEN, chess.BLACK))) == 0:
        white_king = board.king(chess.WHITE)
        black_king = board.king(chess.BLACK)
        if white_king:
            score += (3.5 - chess.square_distance(white_king, chess.E4) * 0.1)
        if black_king:
            score -= (3.5 - chess.square_distance(black_king, chess.E4) * 0.1)

    return score


def minimax(board, depth, is_maximizing_player, alpha, beta):
    if depth == 0 or board.is_game_over():
        eval = evaluate_board(board)
        if board.is_checkmate():
            if is_maximizing_player:
                return eval + depth
            else:
                return eval - depth
        return eval

    if is_maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False, alpha, beta)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True, alpha, beta)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def best_move(board, depth, is_maximizing_player):
    best_move = None
    if is_maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False, float('-inf'), float('inf'))
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True, float('-inf'), float('inf'))
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move

    return best_move


def test_env():
    env = ChessEnv()
    obs = env.reset()

    print("✅ Starting Chess Game:")

    done = False
    depth = 3
    while not done:
        if env.board.turn == chess.WHITE:
            move = best_move(env.board, depth, is_maximizing_player=True)
            print(f"White plays: {move}")
        else:
            move = best_move(env.board, depth, is_maximizing_player=False)
            print(f"Black plays: {move}")

        env.board.push(move)
        obs = env.render()

        done = env.board.is_game_over()

    if env.board.is_checkmate():
        if env.board.turn == chess.WHITE:
            print("Black wins by checkmate!")
        else:
            print("White wins by checkmate!")
    else:
        print("It's a draw (stalemate or insufficient material).")

    print("Game Over!")
    env.close()


if __name__ == "__main__":
    test_env()