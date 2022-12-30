from copy import deepcopy


class PieceUnavailableError(Exception):
    pass


class NotOnBoardError(Exception):
    pass


class CantCoverPieceError(Exception):
    pass


class Game:
    def __init__(self, size) -> None:
        self.__board = []
        for i in range(size):
            self.__board.append([])
            for _ in range(size):
                self.__board[i].append([])
        self.__player_one = []
        self.__player_two = []
        for i in range(size):
            # TODO refactor creating the player's pieces so that the instructions aren't repeated
            self.__player_one.append(('player_one', i + 1))
            self.__player_one.append(('player_one', i + 1))
            self.__player_two.append(('player_two', i + 1))
            self.__player_two.append(('player_two', i + 1))
        self.__recent_boards = []

    def board(self):
        return self.__board

    def set_board(self, new_board):
        self.__board = new_board

    def player_one_pieces(self):
        return self.__player_one

    def set_player_one_pieces(self, new_pieces):
        self.__player_one = new_pieces

    def player_two_pieces(self):
        return self.__player_two

    def set_player_two_pieces(self, new_pieces):
        self.__player_two = new_pieces

    def recent_boards(self):
        return self.__recent_boards

    def update_recent_boards(self):
        current_board = deepcopy(self.board())
        boards = deepcopy(self.recent_boards())
        if len(boards) == 9:
            boards.pop(0)
        boards.append(current_board)
        self.__recent_boards = boards

    def move(self, player, size, previous_position, new_position):
        if player == 'player_one':
            player_pieces = self.player_one_pieces
            set_player_pieces = self.set_player_one_pieces
        else:
            player_pieces = self.player_two_pieces
            set_player_pieces = self.set_player_two_pieces
        if (player, size) not in player_pieces() and previous_position is None:
            raise PieceUnavailableError('This piece is not available!')
        if previous_position is not None:
            try:
                if self.board()[previous_position[1] - 1][previous_position[0] - 1][-1] != (player, size):
                    raise NotOnBoardError('This piece is not on the board!')
            except IndexError:
                raise NotOnBoardError('This piece is not on the board!')
            # TODO get rid of except: pass
            try:
                if size <= self.board()[new_position[1] - 1][new_position[0] - 1][-1][1]:
                    raise CantCoverPieceError('The piece you are trying to cover is larger than your piece!')
            except IndexError:
                pass
        if previous_position is None:
            new_board = deepcopy(self.board())
            new_player_pieces = deepcopy(player_pieces())
            new_board[new_position[1] - 1][new_position[0] - 1].append((player, size))
            new_player_pieces.remove((player, size))
            self.set_board(new_board)
            set_player_pieces(new_player_pieces)
        else:
            new_board = deepcopy(self.board())
            new_player_pieces = deepcopy(player_pieces())
            new_board[new_position[1] - 1][new_position[0] - 1].append((player, size))
            new_board[previous_position[1] - 1][previous_position[0] - 1].pop()
            self.set_board(new_board)
            set_player_pieces(new_player_pieces)
        self.update_recent_boards()

    def check_for_win(self):
        possible_winners = []
        top_layer = []
        for row in self.board():
            new_row = []
            for cell in row:
                try:
                    new_row.append(cell[-1])
                except IndexError:
                    new_row.append(('',))
            top_layer.append(new_row)
        # checking rows
        for row in top_layer:
            row_pieces = []
            for cell in row:
                row_pieces.append(cell[0])
            if len(set(row_pieces)) == 1 and set(row_pieces) != {''}:
                possible_winners.append(row_pieces[0])
        # checking columns
        for i in range(len(top_layer)):
            column_pieces = []
            for j in range(len(top_layer)):
                column_pieces.append(top_layer[j][i][0])
            if len(set(column_pieces)) == 1 and set(column_pieces) != {''}:
                possible_winners.append(column_pieces[0])
        # checking left diagonal
        left_diagonal_pieces = []
        for i in range(len(top_layer)):
            left_diagonal_pieces.append(top_layer[i][i][0])
        if len(set(left_diagonal_pieces)) == 1 and set(left_diagonal_pieces) != {''}:
            possible_winners.append(left_diagonal_pieces[0])
        # checking right diagonal
        right_diagonal_pieces = []
        for i in range(len(top_layer)):
            right_diagonal_pieces.append(top_layer[i][-1 - i][0])
        if len(set(right_diagonal_pieces)) == 1 and set(right_diagonal_pieces) != {''}:
            possible_winners.append(right_diagonal_pieces[0])
        # checking for draw by repetition
        for board in self.recent_boards():
            if self.recent_boards().count(board) == 3:
                return 'Draw'
        # checking for draw or win
        if len(possible_winners) == 0:
            return None
        elif len(possible_winners) == 1:
            return possible_winners[0]
        else:
            return 'Draw'
