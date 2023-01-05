from game import Game
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
        new_piece = input(move_prompt.format(player=''))[0].upper()
        if new_piece == 'T':
            piece_size = input(size_prompt)
            if not piece_size.isnumeric() or int(piece_size) > size:
                error_output = 'Nieprawidłowy rozmiar pionka'
                return
            new_coordinates = input(new_position_prompt).split()[:2]
            if any([int(coordinate) <= 0 or int(coordinate) > size for coordinate in new_coordinates]):
                error_output = 'Nieprawidłowe koordynaty'
        elif new_piece == 'N':
            coordinates = input(position_prompt).split()[:2]
            if any([int(coordinate) <= 0 or int(coordinate) > size for coordinate in coordinates]):
                error_output = 'Nieprawidłowe koordynaty'
                return
            new_coordinates = input(new_position_prompt).split()[:2]
            if any([int(coordinate) <= 0 or int(coordinate) > size for coordinate in new_coordinates]):
                error_output = 'Nieprawidłowe koordynaty'
                return
        else:
            error_output = 'Nieprawidłowy wybór'
            return
    while True:
        os.system('clear')
        print(ui.board())
        print(ui.pieces('player_one'))
        print(ui.pieces('player_two'))
        print(error_output)
        if ai and _round % 2 == 1:
            move('')
        elif ai:
            pass
        elif _round % 2 == 1:
            move(' 1')
        else:
            move(' 2')


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
            size = input('Podaj rozmiar planszy: ')
            if size.isnumeric() and int(size) > 2:
                game(int(size), False)
                break
            else:
                message = 'Nieprawidłowy rozmiar planszy!'
        elif choice == '2':
            message = ''
        else:
            message = 'Nieprawidłowa opcja!'


if __name__ == '__main__':
    main()
