from ai import Ai, CouldNotMoveError
from game import Game
from pytest import raises
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
    mocklist = [returnOne(), returnOne(), returnTwo(), returnTwo(), returnOne(), returnOne()]
    mocks = mock.Mock(side_effect=mocklist)
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


def test_ai_win_top_row():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[('player_two', 1)], [], [('player_two', 1)]],
        [[], [], []],
        [[], [], []]
    ])
    ai.win()
    assert game.board() == [
        [[('player_two', 1)], [('player_two', 3)], [('player_two', 1)]],
        [[], [], []],
        [[], [], []]
    ]


def test_ai_win_middle_row():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [], []],
        [[('player_two', 3)], [('player_two', 3)], []],
        [[], [], []]
    ])
    game.set_player_two_pieces([('player_two', 1),
                                ('player_two', 1),
                                ('player_two', 2),
                                ('player_two', 2)])
    ai.win()
    assert game.board() == [
        [[], [], []],
        [[('player_two', 3)], [('player_two', 3)], [('player_two', 2)]],
        [[], [], []]
    ]


def test_ai_win_bottom_row():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [], []],
        [[], [], []],
        [[], [('player_two', 3)], [('player_two', 2)]]
    ])
    ai.win()
    assert game.board() == [
        [[], [], []],
        [[], [], []],
        [[('player_two', 3)], [('player_two', 3)], [('player_two', 2)]]
    ]


def test_ai_win_left_column():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[('player_two', 2)], [], []],
        [[('player_two', 3)], [], []],
        [[], [], []]
    ])
    ai.win()
    assert game.board() == [
        [[('player_two', 2)], [], []],
        [[('player_two', 3)], [], []],
        [[('player_two', 3)], [], []]
    ]


def test_ai_win_middle_column():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [('player_two', 2)], []],
        [[], [], []],
        [[], [('player_two', 3)], []]
    ])
    ai.win()
    assert game.board() == [
        [[], [('player_two', 2)], []],
        [[], [('player_two', 3)], []],
        [[], [('player_two', 3)], []]
    ]


def test_ai_win_right_column():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [], []],
        [[], [], [('player_two', 2)]],
        [[], [], [('player_two', 3)]]
    ])
    ai.win()
    assert game.board() == [
        [[], [], [('player_two', 3)]],
        [[], [], [('player_two', 2)]],
        [[], [], [('player_two', 3)]]
    ]


def test_ai_win_left_diagonal():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[('player_two', 3)], [], []],
        [[], [('player_two', 2)], []],
        [[], [], []]
    ])
    ai.win()
    assert game.board() == [
        [[('player_two', 3)], [], []],
        [[], [('player_two', 2)], []],
        [[], [], [('player_two', 3)]]
    ]


def test_ai_win_right_diagonal():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [], []],
        [[], [('player_two', 2)], []],
        [[('player_two', 3)], [], []]
    ])
    ai.win()
    assert game.board() == [
        [[], [], [('player_two', 3)]],
        [[], [('player_two', 2)], []],
        [[('player_two', 3)], [], []]
    ]


def test_ai_win_top_row_cover_opponents_piece():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[('player_two', 1)], [('player_one', 1)], [('player_two', 1)]],
        [[], [], []],
        [[], [], []]
    ])
    ai.win()
    assert game.board() == [
        [[('player_two', 1)], [('player_one', 1), ('player_two', 3)], [('player_two', 1)]],
        [[], [], []],
        [[], [], []]
    ]


def test_ai_win_middle_row_cover_opponents_piece():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [], []],
        [[('player_two', 3)], [('player_two', 3)], [('player_one', 1)]],
        [[], [], []]
    ])
    game.set_player_two_pieces([('player_two', 1),
                                ('player_two', 1),
                                ('player_two', 2),
                                ('player_two', 2)])
    ai.win()
    assert game.board() == [
        [[], [], []],
        [[('player_two', 3)], [('player_two', 3)], [('player_one', 1), ('player_two', 2)]],
        [[], [], []]
    ]


def test_ai_win_bottom_row_cover_opponents_piece():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [], []],
        [[], [], []],
        [[('player_one', 1)], [('player_two', 3)], [('player_two', 2)]]
    ])
    ai.win()
    assert game.board() == [
        [[], [], []],
        [[], [], []],
        [[('player_one', 1), ('player_two', 3)], [('player_two', 3)], [('player_two', 2)]]
    ]


def test_ai_win_left_column_cover_opponents_piece():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[('player_two', 2)], [], []],
        [[('player_two', 3)], [], []],
        [[('player_one', 1)], [], []]
    ])
    ai.win()
    assert game.board() == [
        [[('player_two', 2)], [], []],
        [[('player_two', 3)], [], []],
        [[('player_one', 1), ('player_two', 3)], [], []]
    ]


def test_ai_win_middle_column_cover_opponents_piece():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [('player_two', 2)], []],
        [[], [('player_one', 1)], []],
        [[], [('player_two', 3)], []]
    ])
    ai.win()
    assert game.board() == [
        [[], [('player_two', 2)], []],
        [[], [('player_one', 1), ('player_two', 3)], []],
        [[], [('player_two', 3)], []]
    ]


def test_ai_win_right_column_cover_opponents_piece():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [], [('player_one', 1)]],
        [[], [], [('player_two', 2)]],
        [[], [], [('player_two', 3)]]
    ])
    ai.win()
    assert game.board() == [
        [[], [], [('player_one', 1), ('player_two', 3)]],
        [[], [], [('player_two', 2)]],
        [[], [], [('player_two', 3)]]
    ]


def test_ai_win_left_diagonal_cover_opponents_piece():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[('player_two', 3)], [], []],
        [[], [('player_two', 2)], []],
        [[], [], [('player_one', 1)]]
    ])
    ai.win()
    assert game.board() == [
        [[('player_two', 3)], [], []],
        [[], [('player_two', 2)], []],
        [[], [], [('player_one', 1), ('player_two', 3)]]
    ]


def test_ai_win_right_diagonal_cover_opponents_piece():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [], [('player_one', 1)]],
        [[], [('player_two', 2)], []],
        [[('player_two', 3)], [], []]
    ])
    ai.win()
    assert game.board() == [
        [[], [], [('player_one', 1), ('player_two', 3)]],
        [[], [('player_two', 2)], []],
        [[('player_two', 3)], [], []]
    ]


def test_ai_win_by_moving_other_piece_row():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [], []],
        [[], [], [('player_two', 3)]],
        [[], [('player_two', 3)], [('player_two', 2)]]
    ])
    ai.win()
    assert game.board() == [
        [[], [], []],
        [[], [], []],
        [[('player_two', 3)], [('player_two', 3)], [('player_two', 2)]]
    ]


def test_ai_win_by_moving_other_piece_column():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [('player_two', 2)], []],
        [[('player_two', 3)], [], []],
        [[], [('player_two', 3)], []]
    ])
    ai.win()
    assert game.board() == [
        [[], [('player_two', 2)], []],
        [[], [('player_two', 3)], []],
        [[], [('player_two', 3)], []]
    ]


def test_ai_block_row():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [], []],
        [[], [], [('player_two', 3)]],
        [[], [('player_one', 3)], [('player_one', 2)]]
    ])
    ai.block()
    assert game.board() == [
        [[], [], []],
        [[], [], []],
        [[('player_two', 3)], [('player_one', 3)], [('player_one', 2)]]
    ]


def test_ai_block_column():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [('player_one', 2)], []],
        [[('player_two', 3)], [], []],
        [[], [('player_one', 3)], []]
    ])
    ai.block()
    assert game.board() == [
        [[], [('player_one', 2)], []],
        [[], [('player_two', 3)], []],
        [[], [('player_one', 3)], []]
    ]


def test_ai_block_left_diagonal():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[('player_one', 3)], [('player_two', 3)], []],
        [[], [('player_one', 2)], []],
        [[], [], []]
    ])
    ai.block()
    assert game.board() == [
        [[('player_one', 3)], [], []],
        [[], [('player_one', 2)], []],
        [[], [], [('player_two', 3)]]
    ]


def test_ai_block_right_diagonal():
    game = Game(3)
    ai = Ai(game)
    game.set_board([
        [[], [('player_two', 3)], [('player_one', 3)]],
        [[], [('player_one', 2)], []],
        [[], [], []]
    ])
    ai.block()
    assert game.board() == [
        [[], [], [('player_one', 3)]],
        [[], [('player_one', 2)], []],
        [[('player_two', 3)], [], []]
    ]


def test_ai_win_couldnt_move():
    game = Game(3)
    ai = Ai(game)
    with raises(CouldNotMoveError):
        ai.win()
