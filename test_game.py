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


def test_game_first_players_pieces():
    game = Game(3)
    assert game.first_players_pieces() == [
        ('player1', 1), ('player1', 1), ('player1', 2), ('player1', 2), ('player1', 3), ('player1', 3)
    ]


def test_game_second_players_pieces():
    game = Game(3)
    assert game.second_players_pieces() == [
        ('player2', 1), ('player2', 1), ('player2', 2), ('player2', 2), ('player2', 3), ('player2', 3)
    ]


def test_game_set_first_players_pieces():
    game = Game(3)
    game.set_first_players_pieces([
        ('player1', 1), ('playe1r', 3)
    ])
    assert game.first_players_pieces() == [
        ('player1', 1), ('playe1r', 3)
    ]


def test_game_set_opponents_pieces():
    game = Game(3)
    game.set_second_players_pieces([
        ('player2', 1), ('player2', 3)
    ])
    assert game.second_players_pieces() == [
        ('player2', 1), ('player2', 3)
    ]
