import random

class CheckersGame:
    def __init__(self):
        self.board = self.create_board()
        self.current_player = 'X'  # Player 'X' starts
        self.bot_player = 'O'
        self.player_symbols = {'X': 'X', 'O': 'O'}

    def create_board(self):
        board = [[' ' for _ in range(8)] for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 != 0:
                    board[row][col] = 'O'
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 != 0:
                    board[row][col] = 'X'
        return board

    def display_board(self):
        print("  A B C D E F G H")
        for i in range(8):
            print(f"{i + 1} ", end="")
            for j in range(8):
                print(self.board[i][j], end=" ")
            print()

    def get_piece_moves(self, row, col):
        moves = []
        jumps = []
        directions = [(-1, -1), (-1, 1)] if self.board[row][col] == 'X' else [(1, -1), (1, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            jump_r, jump_c = row + 2 * dr, col + 2 * dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr][nc] == ' ':
                    moves.append((nr, nc))
                elif 0 <= jump_r < 8 and 0 <= jump_c < 8 and self.board[nr][nc] == self.player_symbols[self.bot_player if self.current_player == 'X' else 'X'] and self.board[jump_r][jump_c] == ' ':
                    jumps.append((jump_r, jump_c))
        return jumps if jumps else moves

    def get_all_moves(self, player):
        all_moves = []
        all_jumps = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == player:
                    moves = self.get_piece_moves(row, col)
                    for move in moves:
                        if abs(move[0] - row) == 2:  # Jump detected
                            all_jumps.append((row, col, move[0], move[1]))
                        else:
                            all_moves.append((row, col, move[0], move[1]))
        return all_jumps if all_jumps else all_moves

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        if piece != self.current_player:
            return False
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False
        if self.board[end_row][end_col] != ' ':
            return False
        moves = self.get_piece_moves(start_row, start_col)
        return (end_row, end_col) in moves

    def make_move(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = ' '
        self.board[end_row][end_col] = piece
        # Handle jump
        if abs(end_row - start_row) == 2:
            mid_row, mid_col = (start_row + end_row) // 2, (start_col + end_col) // 2
            self.board[mid_row][mid_col] = ' '

    def has_forced_jump(self):
        return len(self.get_all_moves(self.current_player)) > 0 and any(abs(move[2] - move[0]) == 2 for move in self.get_all_moves(self.current_player))

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def bot_move(self):
        valid_moves = self.get_all_moves(self.bot_player)
        if valid_moves:
            start_row, start_col, end_row, end_col = random.choice(valid_moves)
            self.make_move(start_row, start_col, end_row, end_col)

    def play(self):
        while True:
            self.display_board()
            if self.current_player == 'X':
                print(f"Player {self.current_player}'s turn.")
                forced_jump = self.has_forced_jump()
                if forced_jump:
                    print("You have a forced jump! You must jump.")
                move = input("Enter your move (e.g., A3 B4): ").strip().upper()
                if len(move) != 5 or move[2] != ' ':
                    print("Invalid input. Try again.")
                    continue

                start_col = ord(move[0]) - ord('A')
                start_row = int(move[1]) - 1
                end_col = ord(move[3]) - ord('A')
                end_row = int(move[4]) - 1

                if not self.is_valid_move(start_row, start_col, end_row, end_col):
                    print("Invalid move. Try again.")
                    continue

                if forced_jump and abs(end_row - start_row) != 2:
                    print("You must take the jump. Try again.")
                    continue

                self.make_move(start_row, start_col, end_row, end_col)
                self.switch_player()
            else:
                if self.has_forced_jump():
                    print(f"Bot {self.bot_player} has a forced jump and must jump.")
                self.bot_move()
                self.switch_player()


if __name__ == "__main__":
    game = CheckersGame()
    game.play()
