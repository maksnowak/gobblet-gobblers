from game import Game, PieceUnavailableError, CantCoverPieceError, NotOnBoardError
from ui import Interface
from ai import Ai
import os
from sys import platform

def clear():
    if platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def menu(output: str):
    '''Displays the main menu'''
    clear()
    print(f'''
Welcome to Gobblet Gobblers!

1) Play vs Player
2) Play vs Computer

0) Exit

{output}
''', end='')


def game(size, ai: int):
    '''Begins a game'''
    game = Game(size)
    ui = Interface(game, ai)
    _round = 1
    error_output = ''
    move_prompt = 'Player{player}\'s move. Do you want to place a new piece [Y]es/[N]o: '
    size_prompt = 'Enter the piece\'s size: '
    position_prompt = 'Enter the coordinates of a piece you want to move (column first): '
    new_position_prompt = 'Enter the coordinates you want to place your piece at (column first): '

    def move(player: str):
        '''Displays move prompts and handles user input'''
        nonlocal error_output  # necessary for displaying error messages
        try:
            new_piece = input(move_prompt.format(player=player))[0].upper()  # ignores everything but the first character and makes it uppercase in order to avoid executing the same instructions twice
        except IndexError:
            new_piece = ""
        if new_piece == 'Y':
            coordinates = None
            piece_size = input(size_prompt)
            if not piece_size.isnumeric() or int(piece_size) > size or int(piece_size) <= 0:  # checks if the coordinates are within the board and the size is a number
                error_output = 'Incorrect piece size'
                return
            try:
                new_coordinates = [int(coordinate) for coordinate in input(new_position_prompt).split()[:2]]  # ignores everything after the first two coordinates
                if len(new_coordinates) < 2:
                    raise ValueError
            except ValueError:
                error_output = 'Incorrect coordinates'
                return
            if any([int(coordinate) <= 0 or int(coordinate) > size for coordinate in new_coordinates]):  # checks if the coordinates are within the board
                error_output = 'Incorrect coordinates'
                return
        elif new_piece == 'N':
            coordinates = [int(coordinate) for coordinate in input(position_prompt).split()[:2]]  # ignores everything after the first two coordinates
            if any([int(coordinate) <= 0 or int(coordinate) > size for coordinate in coordinates]):
                error_output = 'Incorrect coordinates'
                return
            try:
                piece_size = game.board()[coordinates[1] - 1][coordinates[0] - 1][-1][1]
            except IndexError:
                piece_size = 0
            try:
                new_coordinates = [int(coordinate) for coordinate in input(new_position_prompt).split()[:2]]  # ignores everything after the first two coordinates
                if len(new_coordinates) < 2:
                    raise ValueError
            except ValueError:
                error_output = 'Incorrect coordinates'
                return
            if any([int(coordinate) <= 0 or int(coordinate) > size for coordinate in new_coordinates]):  # checks if the coordinates are within the board
                error_output = 'Incorrect coordinates'
                return
        else:
            error_output = 'Incorrect choice'
            return
        # aliasing the player in order to avoid repeating code
        if ai:
            _player = 'player_one'
        elif not ai and player == ' 1':
            _player = 'player_one'
        else:
            _player = 'player_two'
        try:
            game.move(_player, int(piece_size), coordinates, new_coordinates)
        # handling game engine errors
        except NotOnBoardError:
            error_output = 'There is no piece at given coordinates'
            return
        except PieceUnavailableError:
            error_output = 'You don\'t have that piece'
            return
        except CantCoverPieceError:
            error_output = 'You can\'t place the piece. The piece you\'re trying to cover is too large'
            return
        return True  # the round has completed succesfully

    def game_status():
        '''Displays the board, the player's pieces and error messages if there are any'''
        clear()
        print(ui.board())
        print(ui.pieces('player_one'))
        print(ui.pieces('player_two'))
        print(error_output)

    computer = Ai(game)
    while True:
        game_status()
        # player's turn
        if ai and _round % 2 == 1:
            round_result = move('')
        # computer's turn
        elif ai:
            computer.make_move()
            round_result = True
        # first player's turn
        elif _round % 2 == 1:
            round_result = move(' 1')
        # second player's turn
        else:
            round_result = move(' 2')
        if round_result:
            # declaring the winne
            if ui.winner() is not None:
                error_output = ''
                game_status()
                print(ui.winner())
                input('Press Enter to return to main menu...')
                break
            error_output = ''  # resetting error messages
            _round += 1


def main():
    '''Display's the main menu and handles user's choices'''
    message = ''  # error messages will be saved here

    def game_creation(with_computer: bool):
        nonlocal message
        message = ''
        size = input('Enter the board\'s size (3 to 9): ')
        if size.isnumeric() and int(size) > 2 and int(size) < 10:
            game(int(size), with_computer)
        else:
            message = 'Incorrect board size'
    while True:
        menu(message)
        choice = input('Select one of the options by typing its number ')
        if choice == '0':
            clear()
            break
        elif choice == '1':
            game_creation(False)
        elif choice == '2':
            game_creation(True)
        else:
            message = 'Incorrect option'


if __name__ == '__main__':
    main()
