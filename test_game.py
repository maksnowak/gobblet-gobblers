from game import Game, PieceUnavailableError, NotOnBoardError, CantCoverPieceError
from pytest import raises


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


def test_game_player_one_pieces():
    game = Game(3)
    assert game.player_one_pieces() == [
        ('player_one', 1), ('player_one', 1), ('player_one', 2), ('player_one', 2), ('player_one', 3), ('player_one', 3)
    ]


def test_game_player_two_pieces():
    game = Game(3)
    assert game.player_two_pieces() == [
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 2), ('player_two', 3), ('player_two', 3)
    ]


def test_game_set_player_one_pieces():
    game = Game(3)
    game.set_player_one_pieces([
        ('player_one', 1), ('playe1r', 3)
    ])
    assert game.player_one_pieces() == [
        ('player_one', 1), ('playe1r', 3)
    ]


def test_game_set_player_two_pieces():
    game = Game(3)
    game.set_player_two_pieces([
        ('player_two', 1), ('player_two', 3)
    ])
    assert game.player_two_pieces() == [
        ('player_two', 1), ('player_two', 3)
    ]


def test_game_move_new_piece_check_board():
    game = Game(3)
    game.move('player_one', 2, None, [1, 3])
    assert game.board() == [
        [[], [], []],
        [[], [], []],
        [[('player_one', 2)], [], []]
    ]


def test_game_move_new_piece_check_players_pieces():
    game = Game(3)
    game.move('player_one', 2, None, [1, 3])
    assert game.player_one_pieces() == [
        ('player_one', 1), ('player_one', 1), ('player_one', 2), ('player_one', 3), ('player_one', 3)
    ]


def test_game_move_new_piece_covers_opponents_piece_check_board():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [('player_two', 2)], []],
        [[], [], []]
    ])
    game.set_player_two_pieces([
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 3), ('player_two', 3)
    ])
    game.move('player_one', 3, None, [2, 2])
    assert game.board() == [
        [[], [], []],
        [[], [('player_two', 2), ('player_one', 3)], []],
        [[], [], []]
    ]


def test_game_move_new_piece_covers_opponents_piece_check_pieces():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [('player_two', 2)], []],
        [[], [], []]
    ])
    game.set_player_two_pieces([
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 3), ('player_two', 3)
    ])
    game.move('player_one', 3, None, [2, 2])
    assert game.player_one_pieces() == [
        ('player_one', 1), ('player_one', 1), ('player_one', 2), ('player_one', 2), ('player_one', 3)
    ]


def test_game_move_new_piece_covers_players_own_piece_check_board():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [('player_two', 2)], []],
        [[], [], []]
    ])
    game.set_player_two_pieces([
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 3), ('player_two', 3)
    ])
    game.move('player_two', 3, None, [2, 2])
    assert game.board() == [
        [[], [], []],
        [[], [('player_two', 2), ('player_two', 3)], []],
        [[], [], []]
    ]


def test_game_move_new_piece_covers_players_own_piece_check_pieces():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [('player_two', 2)], []],
        [[], [], []]
    ])
    game.set_player_two_pieces([
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 3), ('player_two', 3)
    ])
    game.move('player_two', 3, None, [2, 2])
    assert game.player_two_pieces() == [
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 3)
    ]


def test_game_move_piece_from_board_check_board():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [], []],
        [[('player_one', 3)], [], []]
    ])
    game.set_player_one_pieces([
        ('player_one', 1), ('player_one', 1), ('player_one', 2), ('player_one', 2), ('player_one', 3)
    ])
    game.move('player_one', 3, [1, 3], [2, 2])
    assert game.board() == [
        [[], [], []],
        [[], [('player_one', 3)], []],
        [[], [], []]
    ]


def test_game_move_piece_from_board_check_pieces():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [], []],
        [[('player_one', 3)], [], []]
    ])
    game.set_player_one_pieces([
        ('player_one', 1), ('player_one', 1), ('player_one', 2), ('player_one', 2), ('player_one', 3)
    ])
    game.move('player_one', 3, [1, 3], [2, 2])
    assert game.player_one_pieces() == [
        ('player_one', 1), ('player_one', 1), ('player_one', 2), ('player_one', 2), ('player_one', 3)
    ]


def test_game_move_piece_from_board_cover_opponents_piece_check_board():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [('player_two', 2)], []],
        [[('player_one', 3)], [], []]
    ])
    game.set_player_one_pieces([
        ('player_one', 1), ('player_one', 1), ('player_one', 2), ('player_one', 2), ('player_one', 3)
    ])
    game.set_player_two_pieces([
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 3), ('player_two', 3)
    ])
    game.move('player_one', 3, [1, 3], [2, 2])
    assert game.board() == [
        [[], [], []],
        [[], [('player_two', 2), ('player_one', 3)], []],
        [[], [], []]
    ]


def test_game_move_piece_from_board_cover_opponents_piece_check_pieces():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [('player_two', 2)], []],
        [[('player_one', 3)], [], []]
    ])
    game.set_player_one_pieces([
        ('player_one', 1), ('player_one', 1), ('player_one', 2), ('player_one', 2), ('player_one', 3)
    ])
    game.set_player_two_pieces([
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 3), ('player_two', 3)
    ])
    game.move('player_one', 3, [1, 3], [2, 2])
    assert game.player_one_pieces() == [
        ('player_one', 1), ('player_one', 1), ('player_one', 2), ('player_one', 2), ('player_one', 3)
    ]


def test_game_move_piece_from_board_cover_players_own_piece_check_board():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [('player_two', 2)], []],
        [[('player_two', 3)], [], []]
    ])
    game.set_player_two_pieces([
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 3)
    ])
    game.move('player_two', 3, [1, 3], [2, 2])
    assert game.board() == [
        [[], [], []],
        [[], [('player_two', 2), ('player_two', 3)], []],
        [[], [], []]
    ]


def test_game_move_piece_from_board_cover_players_own_piece_check_pieces():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [('player_two', 2)], []],
        [[('player_two', 3)], [], []]
    ])
    game.set_player_two_pieces([
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 3)
    ])
    game.move('player_two', 3, [1, 3], [2, 2])
    assert game.player_two_pieces() == [
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 3)
    ]


def test_game_move_piece_unavailable():
    game = Game(3)
    with raises(PieceUnavailableError):
        game.move('player_one', 4, None, [1, 1])


def test_game_move_piece_not_on_board():
    game = Game(3)
    with raises(NotOnBoardError):
        game.move('player_one', 1, [1, 1], [1, 2])


def test_game_move_cant_cover_piece():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [('player_two', 2)], []],
        [[('player_two', 3)], [], []]
    ])
    game.set_player_two_pieces([
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 3)
    ])
    with raises(CantCoverPieceError):
        game.move('player_two', 2, [2, 2], [1, 3])


def test_game_move_cant_cover_piece_both_pieces_are_the_same_size():
    game = Game(3)
    game.set_board([
        [[], [], []],
        [[], [('player_two', 3)], []],
        [[('player_two', 3)], [], []]
    ])
    game.set_player_two_pieces([
        ('player_two', 1), ('player_two', 1), ('player_two', 2), ('player_two', 2)
    ])
    with raises(CantCoverPieceError):
        game.move('player_two', 3, [2, 2], [1, 3])
