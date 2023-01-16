from ui import Interface
from game import Game


def test_interface_board_3_by_3():
    game = Game(3)
    game.move('player_one', 2, None, [1, 3])
    assert Interface(game, False).board() == '''-------------
|   |   |   |
-------------
|   |   |   |
-------------
| 2 |   |   |
-------------
'''


def test_interface_board_4_by_4():
    game = Game(4)
    game.move('player_one', 2, None, [1, 3])
    assert Interface(game, False).board() == '''-----------------
|   |   |   |   |
-----------------
|   |   |   |   |
-----------------
| 2 |   |   |   |
-----------------
|   |   |   |   |
-----------------
'''


def test_interface_pieces_player_one_no_ai():
    game = Game(3)
    assert Interface(game, False).pieces('player_one') == 'Pionki pierwszego gracza: 1, 1, 2, 2, 3, 3'


def test_interface_pieces_player_two_no_ai():
    game = Game(3)
    assert Interface(game, False).pieces('player_two') == 'Pionki drugiego gracza: 1, 1, 2, 2, 3, 3'


def test_interface_pieces_player_one_with_ai():
    game = Game(3)
    assert Interface(game, True).pieces('player_one') == 'Pionki gracza: 1, 1, 2, 2, 3, 3'


def test_interface_pieces_player_two_with_ai():
    game = Game(3)
    assert Interface(game, True).pieces('player_two') == 'Pionki komputera: 1, 1, 2, 2, 3, 3'


def test_interface_winner_no_winner():
    game = Game(3)
    assert Interface(game, False).winner() is None


def test_interface_winner_player_one_with_ai():
    game = Game(3)
    game.set_board([
        [[('player_one', 1)], [('player_one', 2)], [('player_one', 3)]],
        [[], [], []],
        [[], [], []]
    ])
    assert Interface(game, True).winner() == 'Wygrana: Gracz'


def test_interface_winner_player_two_with_ai():
    game = Game(3)
    game.set_board([
        [[('player_two', 1)], [('player_two', 2)], [('player_two', 3)]],
        [[], [], []],
        [[], [], []]
    ])
    assert Interface(game, True).winner() == 'Wygrana: Komputer'


def test_interface_winner_player_one_no_ai():
    game = Game(3)
    game.set_board([
        [[('player_one', 1)], [('player_one', 2)], [('player_one', 3)]],
        [[], [], []],
        [[], [], []]
    ])
    assert Interface(game, False).winner() == 'Wygrana: Gracz 1'


def test_interface_winner_player_two_no_ai():
    game = Game(3)
    game.set_board([
        [[('player_two', 1)], [('player_two', 2)], [('player_two', 3)]],
        [[], [], []],
        [[], [], []]
    ])
    assert Interface(game, False).winner() == 'Wygrana: Gracz 2'


def test_interface_winner_draw_by_repetition():
    game = Game(3)
    game.set_board([
        [[('player_one', 3)], [], []],
        [[], [], []],
        [[('player_two', 3)], [], []]
    ])
    game.update_recent_boards()
    game.move('player_two', 3, [1, 3], [2, 3])
    game.move('player_one', 3, [1, 1], [2, 1])
    game.move('player_two', 3, [2, 3], [1, 3])
    game.move('player_one', 3, [2, 1], [1, 1])
    game.move('player_two', 3, [1, 3], [2, 3])
    game.move('player_one', 3, [1, 1], [2, 1])
    game.move('player_two', 3, [2, 3], [1, 3])
    game.move('player_one', 3, [2, 1], [1, 1])
    assert Interface(game, False).winner() == 'Remis - powtórzenie ruchów'


def test_interface_winner_draw():
    game = Game(3)
    game.set_board([
        [[('player_one', 3)], [('player_one', 3)], [('player_one', 3)]],
        [[], [], []],
        [[('player_two', 2)], [('player_two', 2)], [('player_two', 1)]]
    ])
    assert Interface(game, False).winner() == 'Remis'
