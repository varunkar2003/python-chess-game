import random

class Piece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol

    def valid_moves(self, start, board):
        raise NotImplementedError("This method should be overridden by subclasses")


class King(Piece):
    def __init__(self, color):
        symbol = 'K' if color == 'white' else 'k'
        super().__init__(color, symbol)

    def valid_moves(self, start, board):
        moves = []
        row, col = start
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in directions:
            new_row, new_col = row + d[0], col + d[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
        return moves


class Queen(Piece):
    def __init__(self, color):
        symbol = 'Q' if color == 'white' else 'q'
        super().__init__(color, symbol)

    def valid_moves(self, start, board):
        return Rook(self.color).valid_moves(start, board) + Bishop(self.color).valid_moves(start, board)


class Bishop(Piece):
    def __init__(self, color):
        symbol = 'B' if color == 'white' else 'b'
        super().__init__(color, symbol)

    def valid_moves(self, start, board):
        moves = []
        row, col = start
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            new_row, new_col = row + d[0], col + d[1]
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += d[0]
                new_col += d[1]
        return moves


class Rook(Piece):
    def __init__(self, color):
        symbol = 'R' if color == 'white' else 'r'
        super().__init__(color, symbol)

    def valid_moves(self, start, board):
        moves = []
        row, col = start
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            new_row, new_col = row + d[0], col + d[1]
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += d[0]
                new_col += d[1]
        return moves


class Knight(Piece):
    def __init__(self, color):
        symbol = 'N' if color == 'white' else 'n'
        super().__init__(color, symbol)

    def valid_moves(self, start, board):
        moves = []
        row, col = start
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for d in directions:
            new_row, new_col = row + d[0], col + d[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] is None or board[new_row][new_col].color != self.color:
                    moves.append((new_row, new_col))
        return moves


class Pawn(Piece):
    def __init__(self, color):
        symbol = 'P' if color == 'white' else 'p'
        super().__init__(color, symbol)

    def valid_moves(self, start, board):
        moves = []
        row, col = start
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1

        # Move forward
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))
            # Double move from start position
            if row == start_row and board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))

        # Capturing moves
        for d_col in [-1, 1]:
            if 0 <= col + d_col < 8 and 0 <= row + direction < 8:
                target_piece = board[row + direction][col + d_col]
                if target_piece is not None and target_piece.color != self.color:
                    moves.append((row + direction, col + d_col))

        return moves


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        # Place pawns
        for i in range(8):
            self.board[6][i] = Pawn('white')
            self.board[1][i] = Pawn('black')

        # Place other pieces
        placement = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i in range(8):
            self.board[7][i] = placement[i]('white')
            self.board[0][i] = placement[i]('black')

    def move_piece(self, start, end):
        piece = self.board[start[0]][start[1]]
        target_piece = self.board[end[0]][end[1]]
        if piece is not None and end in piece.valid_moves(start, self.board):
            if isinstance(target_piece, King):
                return 'game_over'
            self.board[end[0]][end[1]] = piece
            self.board[start[0]][start[1]] = None
            return True
        return False

    def get_all_moves(self, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is not None and piece.color == color:
                    piece_moves = piece.valid_moves((row, col), self.board)
                    for move in piece_moves:
                        moves.append(((row, col), move))
        return moves

    def display(self):
        print("  a b c d e f g h")
        for row in range(8):
            print(f"{8 - row} ", end="")
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    print(". ", end="")
                else:
                    print(f"{piece.symbol} ", end="")
            print(f"{8 - row}")
        print("  a b c d e f g h")


class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'
        self.game_mode = None
        self.game_over = False

    def choose_game_mode(self):
        while True:
            choice = input("Do you want to play a 1-player game or a 2-player game? (Enter 1 or 2): ")
            if choice in ['1', '2']:
                self.game_mode = int(choice)
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def play_game(self):
        self.choose_game_mode()
        while not self.game_over:
            self.board.display()
            if self.current_turn == 'white':
                self.player_turn()
                if self.game_over:
                    print("White wins!")
                    break
                self.current_turn = 'black'
            else:
                if self.game_mode == 1:
                    self.computer_move()
                    if self.game_over:
                        print("Black (Computer) wins!")
                        break
                else:
                    self.player_turn()
                    if self.game_over:
                        print("Black wins!")
                        break
                self.current_turn = 'white'

    def player_turn(self):
        print(f"{self.current_turn.capitalize()}'s turn")
        start = input("Enter start position (e.g., e2): ")
        end = input("Enter end position (e.g., e4): ")

        start_pos = (8 - int(start[1]), ord(start[0]) - ord('a'))
        end_pos = (8 - int(end[1]), ord(end[0]) - ord('a'))

        move_result = self.board.move_piece(start_pos, end_pos)
        if move_result == 'game_over':
            self.game_over = True
        elif not move_result:
            print("Invalid move! Please try again.")
            self.player_turn()

    def computer_move(self):
        all_moves = self.board.get_all_moves('black')
        if all_moves:
            start, end = random.choice(all_moves)
            move_result = self.board.move_piece(start, end)
            if move_result == 'game_over':
                self.game_over = True
            print(f"Computer moved from {chr(start[1] + ord('a'))}{8 - start[0]} to {chr(end[1] + ord('a'))}{8 - end[0]}")


if __name__ == "__main__":
    game = ChessGame()
    game.play_game()
