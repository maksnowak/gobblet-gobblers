from game import Game
# from pytest import raises


def test_game_create_3_by_3_board():
    game = Game(3)
    assert game.board() == [
        [[], [], []],
        [[], [], []],
        [[], [], []]
    ]


def test_game_create_4_by_4_board():
    game = Game(4)
    assert game.board() == [
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []]
    ]


def test_game_set_board():
    game = Game(3)
    game.set_board([
        [[1], [2], [3]],
        [[4], [5], [6]],
        [[7], [8], [9]]
    ])
    assert game.board() == [
        [[1], [2], [3]],
        [[4], [5], [6]],
        [[7], [8], [9]]
    ]
