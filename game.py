class Game:
    def __init__(self, size) -> None:
        self.__board = []
        for _ in range(size):
            self.__board.append([[]] * size)
        self.__player = []
        self.__opponent = []
        for i in range(size):
            # TODO refactor creating the player's pieces so that the instructions aren't repeated
            self.__player.append(('player', i + 1))
            self.__player.append(('player', i + 1))
            self.__opponent.append(('opponent', i + 1))
            self.__opponent.append(('opponent', i + 1))

    def board(self):
        return self.__board

    def set_board(self, new_board):
        self.__board = new_board

    def players_pieces(self):
        return self.__player

    def set_players_pieces(self, new_pieces):
        self.__player = new_pieces

    def opponents_pieces(self):
        return self.__opponent

    def set_opponents_pieces(self, new_pieces):
        self.__opponent = new_pieces
