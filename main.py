from game import Game, PieceUnavailableError, CantCoverPieceError, NotOnBoardError
from ui import Interface
import os


def menu(output):
    os.system('clear')
    print(f'''
Witaj w grze Gobblet Gobblers!

1) Gra z drugim graczem
2) Gra z komputerem

0) Wyjdź

{output}
''', end='')


def game(size, ai):
    game = Game(size)
    ui = Interface(game, ai)
    _round = 1
    error_output = ''
    move_prompt = 'Ruch gracza{player}. Czy chcesz postawić nowy pionek? [T]ak/[N]ie: '
    size_prompt = 'Podaj rozmiar pionka: '
    position_prompt = 'Podaj koordynaty pionka, który chcesz przenieść (najpierw podaj numer kolumny, a następnie wiersza): '
    new_position_prompt = 'Podaj koordynaty, na które chcesz postawić pionek (najpierw podaj numer kolumny, a następnie wiersza): '

    def move(player):
        nonlocal error_output
        new_piece = input(move_prompt.format(player=player))[0].upper()
        if new_piece == 'T':
            coordinates = None
            piece_size = input(size_prompt)
            if not piece_size.isnumeric() or int(piece_size) > size or int(piece_size) < 1:
                error_output = 'Nieprawidłowy rozmiar pionka'
                return
            try:
                new_coordinates = [int(coordinate) for coordinate in input(new_position_prompt).split()[:2]]
                if len(new_coordinates) < 2:
                    raise ValueError
            except ValueError:
                error_output = 'Nieprawidłowe koordynaty'
                return
            if any([int(coordinate) <= 0 or int(coordinate) > size for coordinate in new_coordinates]):
                error_output = 'Nieprawidłowe koordynaty'
        elif new_piece == 'N':
            coordinates = [int(coordinate) for coordinate in input(position_prompt).split()[:2]]
            if any([int(coordinate) <= 0 or int(coordinate) > size for coordinate in coordinates]):
                error_output = 'Nieprawidłowe koordynaty'
                return
            try:
                piece_size = game.board()[coordinates[1] - 1][coordinates[0] - 1][-1][1]
            except IndexError:
                piece_size = 0
            try:
                new_coordinates = [int(coordinate) for coordinate in input(new_position_prompt).split()[:2]]
                if len(new_coordinates) < 2:
                    raise ValueError
            except ValueError:
                error_output = 'Nieprawidłowe koordynaty'
                return
            if any([int(coordinate) <= 0 or int(coordinate) > size for coordinate in new_coordinates]):
                error_output = 'Nieprawidłowe koordynaty'
                return
        else:
            error_output = 'Nieprawidłowy wybór'
            return
        if ai:
            _player = 'player_one'
        elif not ai and player == ' 1':
            _player = 'player_one'
        else:
            _player = 'player_two'
        try:
            game.move(_player, int(piece_size), coordinates, new_coordinates)
        except NotOnBoardError:
            error_output = 'Na podanych koordynatach nie znajduje się żaden pionek'
            return
        except PieceUnavailableError:
            error_output = 'Nie masz takiego pionka'
            return
        except CantCoverPieceError:
            error_output = 'Nie możesz postawić pionka! Pionek, który chcesz przykryć jest za duży'
            return
        return True

    def game_status():
        os.system('clear')
        print(ui.board())
        print(ui.pieces('player_one'))
        print(ui.pieces('player_two'))
        print(error_output)

    while True:
        game_status()
        if ai and _round % 2 == 1:
            round_result = move('')
        elif ai:
            pass
        elif _round % 2 == 1:
            round_result = move(' 1')
        else:
            round_result = move(' 2')
        if round_result:
            if ui.winner() is not None:
                game_status()
                print(ui.winner())
                input('Naciśnij Enter, aby powrócić do menu głównego...')
                break
            error_output = ''
            _round += 1


def main():
    message = ''
    while True:
        menu(message)
        choice = input('Wybierz jedną z powyższych opcji wpisując jej numer: ')
        if choice == '0':
            os.system('clear')
            break
        elif choice == '1':
            message = ''
            size = input('Podaj rozmiar planszy (od 3 do 9): ')
            if size.isnumeric() and int(size) > 2 and int(size) < 10:
                game(int(size), False)
            else:
                message = 'Nieprawidłowy rozmiar planszy!'
        elif choice == '2':
            message = ''
        else:
            message = 'Nieprawidłowa opcja!'


if __name__ == '__main__':
    main()
