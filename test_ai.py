from ai import Ai
from game import Game
from unittest import mock


def test_ai_game():
    game = Game(3)
    ai = Ai(game)
    assert ai.game() == game


def test_ai_random_move_new_piece(monkeypatch):
    def returnOne(x, y):
        return 1

    def returnNone(x):
        return None
    monkeypatch.setattr('ai.randint', returnOne)
    monkeypatch.setattr('ai.choice', returnNone)
    game = Game(3)
    ai = Ai(game)
    ai.random_move()
    assert game.board() == [
        [[('player_two', 1)], [], []],
        [[], [], []],
        [[], [], []]
    ]


def test_ai_random_move_piece_from_board(monkeypatch):
    def returnOne():
        return 1

    def returnTwo():
        return 2

    def returnPiece(x):
        return [1, 1]
    # TODO write mocks in a prettier way
    mocks = mock.Mock(side_effect=[returnOne(), returnOne(), returnTwo(), returnTwo(), returnOne(), returnOne()])
    monkeypatch.setattr('ai.randint', mocks)
    monkeypatch.setattr('ai.choice', returnPiece)
    game = Game(3)
    ai = Ai(game)
    game.move('player_two', 1, None, [1, 1])
    ai.random_move()
    assert game.board() == [
        [[], [], []],
        [[], [('player_two', 1)], []],
        [[], [], []]
    ]
