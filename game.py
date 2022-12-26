class Game:
    def __init__(self, size) -> None:
        self.__board = []
        for _ in range(size):
            self.__board.append([[]] * size)
        self.__player_one = []
        self.__player_two = []
        for i in range(size):
            # TODO refactor creating the player's pieces so that the instructions aren't repeated
            self.__player_one.append(('player1', i + 1))
            self.__player_one.append(('player1', i + 1))
            self.__player_two.append(('player2', i + 1))
            self.__player_two.append(('player2', i + 1))

    def board(self):
        return self.__board

    def set_board(self, new_board):
        self.__board = new_board

    def first_players_pieces(self):
        return self.__player_one

    def set_first_players_pieces(self, new_pieces):
        self.__player_one = new_pieces

    def second_players_pieces(self):
        return self.__player_two

    def set_second_players_pieces(self, new_pieces):
        self.__player_two = new_pieces
