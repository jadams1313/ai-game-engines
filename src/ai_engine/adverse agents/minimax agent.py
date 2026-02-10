import math 
import random


class Board:

    def __init__(self, boardValues, current_team):
        self.size = 6
        self.board_values = boardValues
        # Board state: 0 = empty, 1 = Alpha, 2 = Bravo
        self.board_state = [[0] * self.size for _ in range(self.size)]
        self.move_count = 0
        self.current_team = current_team

    def is_gameover(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board_state[i][j] == 0:
                    return False
        return True
    
    def winner(self):
        if not self.is_gameover():
            return None
        
        alpha_score = self.get_score(1)
        bravo_score = self.get_score(2)
        
        if alpha_score > bravo_score:
            return 1
        elif alpha_score < bravo_score:
            return 2
        else:
            return 0 

    def get_valid_moves(self, team):

        moves = []
        #positions controlled by teams
        team_positions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board_state[i][j] == team:
                    team_positions.append((i, j))
        
        #empty tile
        for i in range(self.size):
            for j in range(self.size):
                if self.board_state[i][j] == 0:
                    moves.append(('deploy', i, j))
        
        #move from existing positions
        for i, j in team_positions:
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < self.size and 0 <= nj < self.size:
                    if self.board_state[ni][nj] == 0:
                        would_capture = self.check_captures(ni, nj, team)
                        moves.append(('assault', i, j, ni, nj, would_capture))
        
        return moves
    
    def check_captures(self, i, j, team):
        enemy = 2 if team == 1 else 1

        captures = []
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + di, j + dj #neighbors on the board
            if 0 <= ni < self.size and 0 <= nj < self.size:
                if self.board_state[ni][nj] == enemy:
                    captures.append((ni, nj))
        return captures
    
    def print_board(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if self.board_state[i][j] == 0:
                    row.append(str(self.board_values[i][j]))
                elif self.board_state[i][j] == 1:
                    row.append(f"{self.board_values[i][j]}")
                else:
                    row.append(f"{self.board_values[i][j]}")
            print(','.join(row))

    def push(self, move, team):
        if move[0] == 'deploy':
            _, i, j = move
            self.board_state[i][j] = team
        else:  # assault
            _, si, sj, ti, tj, captures = move
            self.board_state[ti][tj] = team
            #convert
            for ci, cj in captures:
                self.board_state[ci][cj] = team

    def undo(self, move, team):
        if move[0] == 'deploy':
            _, i, j = move
            self.board_state[i][j] = 0
        else:  # assault
            _, si, sj, ti, tj, captures = move
            self.board_state[ti][tj] = 0
            # restore captured
            enemy = 1 if team == 2 else 2
            for ci, cj in captures:
                self.board_state[ci][cj] = enemy

    def get_score(self, team):
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board_state[i][j] == team:
                    score += self.board_values[i][j]
        return score
    
    def format_move(self, move):
        if move[0] == 'deploy':
            _, i, j = move
            return f"Deploy at [{chr(65+i)},{j+1}] (value: {self.board_values[i][j]})" #this looks weird, but python char values convert like this (A, B, C...)
        else:
            _, si, sj, ti, tj, captures = move
            return f"Assault from [{chr(65+si)},{sj+1}] to [{chr(65+ti)},{tj+1}]" 
    
class Engine:
    def __init__(self, ai, foe, level):
        self.ai = ai
        self.foe = foe
        self.max_level = level

    def minimax(self, board: Board, ai_turn: bool, depth: int, alpha: float, beta : float):
        
        if board.is_gameover() or depth >= self.max_level:
            return self.evaluate_board(board, depth), None
        available_moves = board.get_valid_moves(self.ai if ai_turn else self.foe)
        
        if ai_turn:
            max_eval = float('-inf')
            best_move = None
            for move in available_moves:
                board.push(move, self.ai)
                eval = self.minimax(board, False, depth + 1, alpha, beta)[0]
                board.undo(move, self.ai)
                max_eval = max(max_eval, eval)
                if max_eval == eval:
                    best_move = move
                alpha = max(alpha, max_eval)
                if alpha > beta:
                    return max_eval, best_move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in available_moves:
                board.push(move, self.foe)
                eval = self.minimax(board, True, depth + 1, alpha, beta)[0]
                board.undo(move, self.foe)
                min_eval = min(min_eval, eval)
                if min_eval == eval:
                    best_move = move
                beta = min(min_eval, beta)
                if beta < alpha:
                    return min_eval, best_move
            return min_eval, best_move

    def evaluate_board(self, board: Board, depth: int) -> int:
        if board.is_gameover():
            winner = board.winner()
            if winner == self.ai:
                return 10000 - depth  
            elif winner == self.foe:
                return -10000 + depth  
            else:
                return 0
        alpha_score = board.get_score(self.ai)
        bravo_score = board.get_score(self.foe) 
        return alpha_score - bravo_score

    def evaluate_best_move(self, board: Board) -> int:
        best_move = self.minimax(board, True, 0, float('-inf'),
                                 float('inf'))[1]
        return best_move

class Game: 
    def __init__(self, ai, foe, level):
        self.board = None
        self.engine = Engine(ai, foe, level)

    def read_input(self, fileName = 'input.txt'):
        try: 
            with open(fileName, 'r') as file:
                board = file.read().strip()
                values = [int(bi.strip()) for bi in board.replace('\n', ',').split(',') if bi.strip()]
                if len(values) != 36:
                    raise ValueError("Input file must have 36 integers.")

                boardValues = []
                for i in range(6):
                    row = values[i*6:(i+1)*6]
                    boardValues.append(row)
                self.board = Board(boardValues, current_team=1) #change if you want to start with Bravo
        except Exception as e:
            print(f"Error reading input file: {e}")
            return None
    def main(): 
        game = Game(ai=1, foe=2, level=4)
        game.read_input('input.txt')
        while not game.board.is_gameover():
            game.board.move_count += 1
            team_name = "Team-Alpha" if game.board.current_team == 1 else "Team-Bravo"
            
            print(f"\nMove {game.board.move_count}:")

            #game state actions 
            best_move = game.engine.evaluate_best_move(game.board)
            if best_move is None:
                print(f"No valid moves for {team_name}")
                break
            game.board.push(best_move, game.board.current_team)
            
            #display
            print(f"Minimax action for {team_name}: {game.board.format_move(best_move)}")
            game.board.print_board()
            alpha_score = game.board.get_score(1)
            bravo_score = game.board.get_score(2)
            print(f"Total score for Alpha: {alpha_score}")
            print(f"Total score for Bravo: {bravo_score}")
            
            #swtich teams
            game.board.current_team = 1 if game.board.current_team == 2 else 2
            game.engine.ai, game.engine.foe = game.engine.foe, game.engine.ai
            
        if game.board.winner() == 1:
            print("The Winner is: Team Alpha")
        elif game.board.winner() == 2:
            print("The Winner is: Team Bravo")
        else:
            print("The game is a tie")
        
if __name__ == "__main__":
    Game.main()