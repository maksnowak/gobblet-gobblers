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


def test_game_players_pieces():
    game = Game(3)
    assert game.players_pieces() == [
        ('player', 1), ('player', 1), ('player', 2), ('player', 2), ('player', 3), ('player', 3)
    ]


def test_game_opponents_pieces():
    game = Game(3)
    assert game.opponents_pieces() == [
        ('opponent', 1), ('opponent', 1), ('opponent', 2), ('opponent', 2), ('opponent', 3), ('opponent', 3)
    ]


def test_game_set_players_pieces():
    game = Game(3)
    game.set_players_pieces([
        ('player', 1), ('player', 3)
    ])
    assert game.players_pieces() == [
        ('player', 1), ('player', 3)
    ]


def test_game_set_opponents_pieces():
    game = Game(3)
    game.set_opponents_pieces([
        ('opponent', 1), ('opponent', 3)
    ])
    assert game.opponents_pieces() == [
        ('opponent', 1), ('opponent', 3)
    ]
