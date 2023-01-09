from game import Game, PieceUnavailableError, CantCoverPieceError, NotOnBoardError
from random import randint, choice


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

    def make_move(self):
        self.random_move()
