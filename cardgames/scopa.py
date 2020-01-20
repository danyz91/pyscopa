from cardgames.decks import decks
from cardgames.player import Player
from cardgames.renderer import GameRenderer
import cardgames.utils as utils
from cardgames.utils import NULL_CARD_VALUE
from cardgames.basic_ai_player import BasicAIPlayer
from cardgames.human_player import HumanPlayer


import random
import time



class Scopa():


    def __init__(self, gui=False, verbose=False):
        self.deck = decks['napolitan']
        self.players = list()
        self.playing_surface = list()
        self.n_players = 0
        self.n_turns = 0
        self.HAND_SIZE = 3
        self.FOUR_PLAYER_HAND_SIZE = 10
        self.MAX_PLAYING_SURFACE_SIZE = 10
        self.evolution_history=list()
        self.leaderboard = dict()
        self.gui = gui
        self.verbose = verbose
        self.renderer = None
        self.players_order = None

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

        self.PRIMIERA_ORDER = {7: 0, 6: 1, 1: 2, 5: 3, 4: 4, 3: 5, 2: 6, 8: 7, 9: 8, 10: 9}

        deck_size = len(self.deck)
        

        
        #self.reset()

    def _get_obs(self, player):
        list_obs = list()
        # first three values
        for card in player.hand:
            list_obs.append(card.abs_value)
        if len(player.hand) < self.HAND_SIZE:
            for i in range(self.HAND_SIZE-len(player.hand)):
                list_obs.append(NULL_CARD_VALUE)

        for card in self.playing_surface:
            list_obs.append(card.abs_value)
        if len(self.playing_surface) < self.MAX_PLAYING_SURFACE_SIZE:
            for i in range(self.MAX_PLAYING_SURFACE_SIZE-len(self.playing_surface)):
                list_obs.append(NULL_CARD_VALUE)

        return tuple(list_obs)

    

    def init_game(self, n_players, human=False):
        """
        Initialize a game, creating players, leaderboards, shuffling deck and init playing surface
        :param n_players: number of players of the game. Default is 2
        :param human: boolean signaling if human game must be set
        :return:
        """
        if n_players == 2:
            self.players_order = [0, 1]
        elif n_players == 3:
            self.players_order = [0, 1, 2]
        elif n_players == 4:
            self.players_order = [0, 3, 1, 2]
        else:
            print('Wrong number of players specified')
            exit(0)

        for i in range(n_players):
            if i == 1:
                # Last player is human or AI, basing on human parameter
                if human:
                    self.players.append(HumanPlayer('Human'))
                else:
                    self.players.append(BasicAIPlayer(utils.generate_random_string()))
            else:
                self.players.append(BasicAIPlayer(utils.generate_random_string()))


        # Init renderer
        if self.gui:
            self.renderer = GameRenderer(self.deck, self.players)

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
        else:
            self.HAND_SIZE = self.FOUR_PLAYER_HAND_SIZE

    def evolve(self, player, player_cards_selected):

        """
            The function handles the action selected by player specified via
            the param player_cards_selected
            :param player, the player that is currently selecting cards
            :param player_cards_selected a list of selected cards, WITH HAND CARDS AT INDEX 0
            :return True if player take something
        """
        obs = self._get_obs(player)
        #print(obs)
        hand_card_selected = player_cards_selected[0]
        player.hand.remove(hand_card_selected)

        # If player plays only one cards, he cannot take anything and his card is added to
        # playing surface
        if len(player_cards_selected) == 1:
            self.playing_surface.append(player_cards_selected[0])
            return False

        # Cards taken are added to player gained cards
        for i in range(len(player_cards_selected)-1):
            player.gained_cards.append(player_cards_selected[i+1])
            self.playing_surface.remove(player_cards_selected[i+1])

        # Check scopa condition
        if len(self.playing_surface) == 0:
            player.pure_points += 1

        # the played card is added to player gained cars
        player.gained_cards.append(hand_card_selected)

        return True

    def print_status(self):
        """
        print the status of the game, playing surface and players hands
        :return:
        """

        print('Turn ', self.n_turns)

        for player in self.players:
            print(player)

        print('Playing surface : ')
        for card in self.playing_surface:
            print(card)

    def deal_cards(self):
        for player in self.players:
            for j in range(self.HAND_SIZE):
                player.hand.append(self.deck.pop())

    def turn(self):
        """
        The function handles one turn. It deal cards and wait for all the player to complete their hand
        :return:
        """

        self.deal_cards()

        if self.gui:
            self.renderer.render(self.playing_surface, self.players)
        
        if self.verbose:
            self.print_status()

        # Wait for everyone to play. Append evolution result to evolution_history
        for k in range(self.HAND_SIZE):
            for curr_index in self.players_order:
                player_cards_selected = self.players[curr_index].act(self.playing_surface, self.verbose)

                if self.gui:
                    time.sleep(1)

                has_taken = self.evolve(self.players[curr_index], player_cards_selected)
                self.evolution_history.append((self.players[curr_index].name, has_taken))

                if self.gui:
                    self.renderer.render(self.playing_surface, self.players, curr_index)

        self.n_turns += 1

    def compute_primiera(self, players):
        """
        For all players apply primiera rules to compute their score
        :param players: list of players of the game
        :return: a dict with (k: player.name, value: primiera_score)
        """

        primiera_leaderboard = dict()
        for player in players:
            primiera_leaderboard[player.name] = 0

        for player in players:
            curr_name = player.name
            curr_score = 0
            # get a list of all suits of each player
            values = set(map(lambda x: x.suit, player.gained_cards))
            # group cards by suit
            cards_by_suit = [[y for y in player.gained_cards if y.suit == x] for x in values]
            # iterate over all suit group, sort by primiera comparison order and take the primiera
            # score of the first card
            for suit_list in cards_by_suit:
                if len(suit_list) != 0:
                    suit_list.sort(key=lambda val: self.PRIMIERA_ORDER[val.value])
                    curr_score += self.PRIMIERA_SCORE[suit_list[0].value]

            primiera_leaderboard[curr_name] = curr_score

        return primiera_leaderboard

    def compute_point(self, dictionary):
        """
        Taking in input the given dictionary, the function updates overall leaderboard
        The functions checks for DRAW condition on given point. In the case, it does not update
        overall leaderboard
        :param dictionary: a dictionary with (k: player.name, value: a point score)
        :return:
        """
        expected_value = next(iter(dictionary.values()))  # check for an empty dictionary first if that's possible
        all_equal = all(value == expected_value for value in dictionary.values())

        if not all_equal:
            self.leaderboard[max(zip(dictionary.values(), dictionary.keys()))[1]] += 1

    def compute_score(self):
        """
        The function compute the overall score of the game computing denari, carte a lungo,
        setteoro e primiera and adding scope gained during game
        :return: the final leaderboard with (k: player.name, value: overall score)
        """
        # Compute Denari
        denari_leaderbord = dict()
        lungo_leaderbord = dict()
        setteoro_leaderbord = dict()

        if self.n_players == 4:
            print('Team 1. Members : ', self.players[0].name, ' and ', self.players[1].name)
            print('Team 2. Members : ', self.players[2].name, ' and ', self.players[3].name)

            self.players[0].gained_cards.extend(self.players[1].gained_cards)
            self.players[2].gained_cards.extend(self.players[3].gained_cards)

            self.players[0].pure_points += self.players[1].pure_points
            self.players[2].pure_points += self.players[3].pure_points
            del (self.leaderboard[self.players[1].name])
            del (self.leaderboard[self.players[3].name])

            self.players.remove(self.players[1])
            self.players.remove(self.players[-1])

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

        print("Denari:")
        print(denari_leaderbord)
        print("Carte a lungo:")
        print(lungo_leaderbord)
        print("Sette Denari:")
        print(setteoro_leaderbord)
        print("Primiera:")
        print(primiera_leaderboard)

        for player in self.players:
            print(player.name, ' has made ', player.pure_points, ' scope ')
            self.leaderboard[player.name] += player.pure_points
        
        print("\nFinal standings:")
        print(self.leaderboard)

        return self.leaderboard

    def start_game(self):
        """
        The main loop of the game
        :return:
        """

        while len(self.deck) != 0 and all(len(player.hand)==0 for player in self.players):
            self.turn()

        # Last player that has taken will take all cards on playing surface
        if len(self.playing_surface) != 0:
            self.evolution_history.reverse()
            last_taken_index = len(self.evolution_history) - 1 - [curr_record[1] for curr_record in self.evolution_history].index(True)

            last_player_taken = self.evolution_history[last_taken_index][0]

            last_player = [player for player in self.players if player.name == last_player_taken][0]
            last_player.gained_cards.extend(self.playing_surface)
            self.playing_surface.clear()

        # End game status
        print('Game Ended!')
        if self.verbose:
            print('Player status : ')
            for player in self.players:
                print(player.name)
                for card in player.gained_cards:
                    print(card)

        self.compute_score()
        if self.gui:
            self.renderer.close_gui()

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
