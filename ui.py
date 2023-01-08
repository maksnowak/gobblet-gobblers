from game import Game
from termcolor import colored


class Interface:
    '''Takes in a Game object and a boolean value whether the player plays against another player or the computer'''
    def __init__(self, game: Game, ai: bool) -> None:
        self.__game = game
        self.__ai = ai

    def game(self):
        '''Returns the Game object'''
        return self.__game

    def ai(self):
        '''Returns information whether the player plays against another player or the computer as a boolean value'''
        return self.__ai

    def board(self):
        '''Generates the board's view with pieces displayed as an integer with the piece's size (red - player, blue - second player / computer)'''
        string = '----' * self.game().size() + '-\n'  # top border
        for row in self.game().board():
            for cell in row:
                # generating pieces or an empty space if there are none
                try:
                    if cell[-1][0] == 'player_one':
                        color = 'red'
                    elif cell[-1][0] == 'player_two':
                        color = 'blue'
                    piece = colored(cell[-1][1], color)
                except IndexError:
                    piece = ' '
                string += f'| {piece} '
            string += '|\n' + '----' * self.game().size() + '-\n'  # bottom border
        return string

    def pieces(self, player):
        '''Takes in the player whose pieces will be shown. Returns a list of the given player's pieces (the pieces are colored the same as on the board)'''
        # aliasing player's pieces list in order to avoid repeating code
        if player == 'player_one':
            pieces_list = self.game().player_one_pieces()
        else:
            pieces_list = self.game().player_two_pieces()
        pieces_string = ', '.join([str(piece[1]) for piece in pieces_list])  # a user-friendly version of the list of pieces
        if self.ai():
            if player == 'player_one':
                return 'Pionki gracza: ' + colored(pieces_string, 'red')
            else:
                return 'Pionki komputera: ' + colored(pieces_string, 'blue')
        else:
            if player == 'player_one':
                return 'Pionki pierwszego gracza: ' + colored(pieces_string, 'red')
            else:
                return 'Pionki drugiego gracza: ' + colored(pieces_string, 'blue')

    def winner(self):
        '''Returns a string with information who won the game (or if it is a draw). If the game cannot be settled yet, returns None'''
        result = self.game().check_for_win()
        if result is None:
            return
        elif result == 'player_one' and self.ai():
            return 'Wygrana: Gracz'
        elif result == 'player_one' and not self.ai():
            return 'Wygrana: Gracz 1'
        elif result == 'player_two' and self.ai():
            return 'Wygrana: Komputer'
        elif result == 'player_two' and not self.ai():
            return 'Wygrana: Gracz 2'
        else:
            return 'Remis'
