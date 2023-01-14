from game import Game, PieceUnavailableError, CantCoverPieceError, NotOnBoardError
from random import randint, choice


class CouldNotMoveError(Exception):
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

    def complete_row(self, player):
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
                if len(set(row_pieces)) == 2 and row_pieces.count(player) == 2:
                    old_coordinates = None
                    try:
                        coordinates = [row_pieces.index('') + 1, i + 1]
                    except ValueError:
                        coordinates = [row_pieces.index('player_one') + 1, i + 1]
                    try:
                        cell_size = board[coordinates[0]][coordinates[1]][-1][1]
                    except IndexError:
                        cell_size = 0
                    for j, top_layer_row in enumerate(self.game().top_layer()):
                        if j == i:
                            continue
                        for k, cell in enumerate(top_layer_row):
                            if cell[0] == 'player_two' and cell[1] > cell_size:
                                old_coordinates = [k + 1, j + 1]
                                break
                        else:
                            continue
                        break
                    self.game().move('player_two', largest_piece, old_coordinates, coordinates)
                    return True
        # checking columns
        for i in range(len(board)):
            column_pieces = []
            for j in range(len(board)):
                try:
                    column_pieces.append(board[j][i][-1][0])
                except IndexError:
                    column_pieces.append('')
            if len(set(column_pieces)) == 2 and column_pieces.count(player) == 2:
                old_coordinates = None
                try:
                    coordinates = [i + 1, column_pieces.index('') + 1]
                except ValueError:
                    coordinates = [i + 1, column_pieces.index('player_one') + 1]
                try:
                    cell_size = board[coordinates[0]][coordinates[1]][-1][1]
                except IndexError:
                    cell_size = 0
                for k in range(len(board)):
                    if k == i:
                        continue
                    for l in range(len(board)):  # noqa: E741
                        try:
                            cell = board[l][k][-1]
                        except IndexError:
                            cell = ('', 0)
                        if cell[0] == 'player_two' and cell[1] > cell_size:
                            old_coordinates = [k + 1, l + 1]
                            break
                    else:
                        continue
                    break
                self.game().move('player_two', largest_piece, old_coordinates, coordinates)
                return True
        # checking left diagonal
        left_diagonal_pieces = []
        for i in range(len(board)):
            try:
                left_diagonal_pieces.append(board[i][i][-1][0])
            except IndexError:
                left_diagonal_pieces.append('')
        if len(set(left_diagonal_pieces)) == 2 and left_diagonal_pieces.count(player) == 2:
            old_coordinates = None
            try:
                coordinates = [left_diagonal_pieces.index('') + 1] * 2
            except ValueError:
                coordinates = [left_diagonal_pieces.index('player_one') + 1] * 2
            try:
                cell_size = board[coordinates[0]][coordinates[1]][-1][1]
            except IndexError:
                cell_size = 0
            if player == 'player_one':
                for j in range(len(board)):
                    for k in range(len(board)):
                        try:
                            cell = board[j][k][-1]
                        except IndexError:
                            cell = ('', 0)
                        if cell[0] == 'player_two' and cell[1] > cell_size:
                            old_coordinates = [k + 1, j + 1]
                            break
                    else:
                        continue
                    break
            self.game().move('player_two', largest_piece, old_coordinates, coordinates)
            return True
        # checking right diagonal
        right_diagonal_pieces = []
        for i in range(len(board)):
            try:
                right_diagonal_pieces.append(board[i][-1 - i][-1][0])
            except IndexError:
                right_diagonal_pieces.append('')
        if len(set(right_diagonal_pieces)) == 2 and right_diagonal_pieces.count(player) == 2:
            old_coordinates = None
            try:
                coordinates = [-1 * right_diagonal_pieces.index('') + 3, right_diagonal_pieces.index('') + 1]
            except ValueError:
                coordinates = [-1 * right_diagonal_pieces.index('player_one') + 3, right_diagonal_pieces.index('player_one') + 1]
            try:
                cell_size = board[coordinates[0]][coordinates[1]][-1][1]
            except IndexError:
                cell_size = 0
            if player == 'player_one':
                for j in range(len(board)):
                    for k in range(len(board)):
                        try:
                            cell = board[j][k][-1]
                        except IndexError:
                            cell = ('', 0)
                        if cell[0] == 'player_two' and cell[1] > cell_size:
                            old_coordinates = [k + 1, j + 1]
                            break
                    else:
                        continue
                    break
            self.game().move('player_two', largest_piece, old_coordinates, coordinates)
            return True
        return False

    def win(self):
        if not self.complete_row('player_two'):
            raise CouldNotMoveError('There isn\'t any winning move')

    def block(self):
        if not self.complete_row('player_one'):
            raise CouldNotMoveError('There isn\'t any winning move')

    def make_move(self):
        moved = False
        try:
            self.win()
            moved = True
        except (NotOnBoardError, PieceUnavailableError, CantCoverPieceError, CouldNotMoveError):
            moved = False
        if not moved:
            try:
                self.block()
                moved = True
            except (NotOnBoardError, PieceUnavailableError, CantCoverPieceError, CouldNotMoveError):
                moved = False
        if not moved:
            self.random_move()
