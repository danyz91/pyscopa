from cardgames.decks import decks
from cardgames.player import Player
import cardgames.utils as utils

import random

class Scopa:

    def __init__(self):
        self.deck = decks['napolitan']
        self.players = list()
        self.playing_surface = list()
        self.n_players = 0
        self.n_turns = 0
        self.HAND_SIZE = 3
        self.evolution_history=list()
        self.leaderboard = dict()


        self.PRIMIERA_SCORE = dict()
        self.PRIMIERA_SCORE[7] = 21
        self.PRIMIERA_SCORE[6] = 18
        self.PRIMIERA_SCORE[1] = 16
        self.PRIMIERA_SCORE[5] = 15
        self.PRIMIERA_SCORE[4] = 14
        self.PRIMIERA_SCORE[3] = 13
        self.PRIMIERA_SCORE[2] = 12
        self.PRIMIERA_SCORE[8] = 10
        self.PRIMIERA_SCORE[9] = 10
        self.PRIMIERA_SCORE[10] = 10

    def init_game(self, n_players=2):
        for i in range(n_players):
            self.players.append(Player(utils.generate_random_string()))
        self.n_players = n_players
        for player in self.players:
            self.leaderboard[player.name] = 0


        # shuffle the deck
        random.shuffle(self.deck)

        # init playing surface with 4 cards
        if n_players != 4:
            self.playing_surface.append(self.deck.pop())
            self.playing_surface.append(self.deck.pop())
            self.playing_surface.append(self.deck.pop())
            self.playing_surface.append(self.deck.pop())


    def evolve(self, player, player_cards_selected):

        '''
            :param player, the player that is currently selecting cards
            :param player_cards_selected a list of selected cards, WITH HAND CARDS AT INDEX 0
            :return True if player take something
        '''

        hand_card_selected = player_cards_selected[0]
        player.hand.remove(hand_card_selected)

        print('Player : ', player.name, ' choices to play ', hand_card_selected)

        if len(player_cards_selected) == 1:
            self.playing_surface.append(player_cards_selected[0])
            return False

        for i in range(len(player_cards_selected)-1):
            player.gained_cards.append(player_cards_selected[i+1])
            self.playing_surface.remove(player_cards_selected[i+1])

        # Check scopa condition
        if len(self.playing_surface)==0:
            player.pure_points += 1

        player.gained_cards.append(hand_card_selected)

        return True

    def turn(self):

        print('Turn ', self.n_turns)
        for i in range(self.n_players):
            for j in range(self.HAND_SIZE):
                self.players[i].hand.append(self.deck.pop())

        for player in self.players:
            print(player)

        print('Playing surface : ')
        for card in self.playing_surface:
            print(card)

        for k in range(self.HAND_SIZE):
            for i in range(self.n_players):
                player_cards_selected = self.players[i].act(self.playing_surface)
                has_taken = self.evolve(self.players[i], player_cards_selected)
                self.evolution_history.append((self.players[i].name, has_taken))

        self.n_turns += 1


    def compute_primiera(self, players):

        primiera_leaderboard = dict()
        for player in players:
            primiera_leaderboard[player.name] = 0

        for player in players:
            curr_name = player.name
            curr_score = 0
            for card in player.gained_cards:
                curr_score += self.PRIMIERA_SCORE[card.value]
            primiera_leaderboard[curr_name] = curr_score

        return primiera_leaderboard

    def compute_point(self, dictionary):
        expected_value = next(iter(dictionary.values()))  # check for an empty dictionary first if that's possible
        all_equal = all(value == expected_value for value in dictionary.values())

        if not all_equal:
            self.leaderboard[max(zip(dictionary.values(), dictionary.keys()))[1]] += 1
        else:
            print(dictionary, " patta ")

    def compute_score(self):
        # Compute Denari
        denari_leaderbord = dict()
        lungo_leaderbord = dict()
        setteoro_leaderbord = dict()

        for player in self.players:
            denari_leaderbord[player.name] = sum(card.suit == 'denari' for card in player.gained_cards)

        # Compute Carte a Lungo
        for player in self.players:
            lungo_leaderbord[player.name] = len(player.gained_cards)

        # Compute Sette Oro
        for player in self.players:
            setteoro_leaderbord[player.name] = any(card.suit == 'denari' and card.value == 7 for card in player.gained_cards)

        primiera_leaderboard = self.compute_primiera(self.players)

        self.compute_point(denari_leaderbord)
        self.compute_point(lungo_leaderbord)
        self.compute_point(setteoro_leaderbord)
        self.compute_point(primiera_leaderboard)

        print(denari_leaderbord)
        print(lungo_leaderbord)
        print(setteoro_leaderbord)
        print(primiera_leaderboard)

        for player in self.players:
            print(player.name, ' has made ', player.pure_points, ' scope ')
            self.leaderboard[player.name] += player.pure_points

        print(self.leaderboard)

    def start_game(self):

        while len(self.deck) != 0:
            self.turn()

        if len(self.playing_surface) != 0:
            self.evolution_history.reverse()
            last_taken_index = len(self.evolution_history) - 1 - [curr_record[1] for curr_record in self.evolution_history].index(True)

            last_player_taken = self.evolution_history[last_taken_index][0]

            last_player = [player for player in self.players if player.name == last_player_taken][0]
            last_player.gained_cards.extend(self.playing_surface)
            self.playing_surface.clear()


        print('Game Ended!')
        print('Player status : ')
        for player in self.players:
            print(player.name)
            for card in player.gained_cards:
                print(card)

        self.compute_score()



    def __str__(self):
        out=''
        out+='Players : '+'\n'
        for i in range(self.n_players):
            out+=str(self.players[i])
        out+='\n'
        out+='Turns playerd : '+str(self.n_turns)
        out += '\n'
        out+='Playing Surface : '
        out += '\n'
        for i in range(len(self.playing_surface)):
            out += str(self.playing_surface[i])
        return out