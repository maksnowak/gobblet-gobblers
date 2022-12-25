class Game:
    def __init__(self, size) -> None:
        self.__board = []
        for _ in range(size):
            self.__board.append([[]] * size)

    def board(self):
        return self.__board

    def set_board(self, new_board):
        self.__board = new_board
