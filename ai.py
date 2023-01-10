from game import Game, PieceUnavailableError, CantCoverPieceError, NotOnBoardError
from random import randint, choice


class CouldNotWinError(Exception):
    pass


class Ai:
    def __init__(self, game: Game) -> None:
        self.__game = game

    def game(self):
        return self.__game

    def random_move(self):
        size = self.game().size()
        while True:
            coordinates = [randint(1, size), randint(1, size)]
            new_coordinates = [randint(1, size), randint(1, size)]
            piece = choice([coordinates, None])
            try:
                if piece is None:
                    piece_size = randint(1, size)
                else:
                    piece_size = self.game().board()[coordinates[1] - 1][coordinates[0] - 1][-1][1]
                self.game().move('player_two', piece_size, piece, new_coordinates)
                break
            except (PieceUnavailableError, CantCoverPieceError, NotOnBoardError, IndexError):
                pass

    def win(self):
        board = self.game().board()
        largest_piece = max(self.game().player_two_pieces())[1]
        # checking rows
        for i, row in enumerate(board):
            row_pieces = []
            for cell in row:
                try:
                    row_pieces.append(cell[-1][0])
                except IndexError:
                    row_pieces.append('')
            if len(set(row_pieces)) == 2 and row_pieces.count('player_two') == 2:
                try:
                    coordinates = [row_pieces.index('') + 1, i + 1]
                except ValueError:
                    coordinates = [row_pieces.index('player_one') + 1, i + 1]
                self.game().move('player_two', largest_piece, None, coordinates)
                return
        # checking columns
        for i in range(len(board)):
            column_pieces = []
            for j in range(len(board)):
                try:
                    column_pieces.append(board[j][i][-1][0])
                except IndexError:
                    column_pieces.append('')
            if len(set(column_pieces)) == 2 and column_pieces.count('player_two') == 2:
                try:
                    coordinates = [i + 1, column_pieces.index('') + 1]
                except ValueError:
                    coordinates = [i + 1, column_pieces.index('player_one') + 1]
                self.game().move('player_two', largest_piece, None, coordinates)
                return
        # checking left diagonal
        left_diagonal_pieces = []
        for i in range(len(board)):
            try:
                left_diagonal_pieces.append(board[i][i][-1][0])
            except IndexError:
                left_diagonal_pieces.append('')
        if len(set(left_diagonal_pieces)) == 2 and left_diagonal_pieces.count('player_two') == 2:
            try:
                coordinates = [left_diagonal_pieces.index('') + 1] * 2
            except ValueError:
                coordinates = [left_diagonal_pieces.index('player_one') + 1] * 2
            self.game().move('player_two', largest_piece, None, coordinates)
            return
        # checking right diagonal
        right_diagonal_pieces = []
        for i in range(len(board)):
            try:
                right_diagonal_pieces.append(board[i][-1 - i][-1][0])
            except IndexError:
                right_diagonal_pieces.append('')
        if len(set(right_diagonal_pieces)) == 2 and right_diagonal_pieces.count('player_two') == 2:
            try:
                coordinates = [right_diagonal_pieces.index(''), right_diagonal_pieces.index('') + 1]
            except ValueError:
                coordinates = [right_diagonal_pieces.index('player_one'), right_diagonal_pieces.index('player_one') + 1]
            self.game().move('player_two', largest_piece, None, coordinates)
            return
        raise CouldNotWinError('There isn\'t any winning move')

    def make_move(self):
        try:
            self.win()
        except (PieceUnavailableError, NotOnBoardError, CantCoverPieceError, CouldNotWinError):
            self.random_move()
