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
            new_board = self.board().copy()
            new_player_pieces = player_pieces().copy()
            new_board[new_position[1] - 1][new_position[0] - 1].append((player, size))
            new_player_pieces.remove((player, size))
            self.set_board(new_board)
            set_player_pieces(new_player_pieces)
        else:
            new_board = self.board().copy()
            new_player_pieces = player_pieces().copy()
            new_board[new_position[1] - 1][new_position[0] - 1].append((player, size))
            new_board[previous_position[1] - 1][previous_position[0] - 1].pop()
            self.set_board(new_board)
            set_player_pieces(new_player_pieces)
