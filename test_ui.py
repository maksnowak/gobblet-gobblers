from ui import Interface
from game import Game


def test_interface_board_3_by_3():
    game = Game(3)
    game.move('player_one', 2, None, [1, 3])
    assert Interface(game).board() == '''-------------
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
    assert Interface(game).board() == '''-----------------
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
    assert Interface(game).pieces('player_one', False) == 'Pionki pierwszego gracza: 1, 1, 2, 2, 3, 3'


def test_interface_pieces_player_two_no_ai():
    game = Game(3)
    assert Interface(game).pieces('player_two', False) == 'Pionki drugiego gracza: 1, 1, 2, 2, 3, 3'


def test_interface_pieces_player_one_with_ai():
    game = Game(3)
    assert Interface(game).pieces('player_one', True) == 'Pionki gracza: 1, 1, 2, 2, 3, 3'


def test_interface_pieces_player_two_with_ai():
    game = Game(3)
    assert Interface(game).pieces('player_two', True) == 'Pionki komputera: 1, 1, 2, 2, 3, 3'
