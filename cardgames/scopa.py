from cardgames.decks import decks
from cardgames.player import Player
from cardgames.game import GameRenderer
import cardgames.utils as utils
from cardgames.basic_ai_player import BasicAIPlayer
from cardgames.human_player import HumanPlayer

import gym
from gym import spaces
from gym.utils import seeding

import random
import time


class Scopa(gym.Env):

    '''
    def step(self, action):
        pass

    def reset(self):
        #obs = list()
        #self.init_game()
        #return obs
        pass


    def render(self, mode='human'):
        pass
    '''

    def __init__(self, gui=False):
        self.deck = decks['napolitan']
        self.players = list()
        self.playing_surface = list()
        self.n_players = 0
        self.n_turns = 0
        self.HAND_SIZE = 3
        self.MAX_PLAYING_SURFACE_SIZE = 10
        self.evolution_history=list()
        self.leaderboard = dict()
        self.gui = gui

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
        self.action_space = spaces.Tuple((
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size)))

        self.observation_space = spaces.Tuple((
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),
            spaces.Discrete(deck_size),))

        self.NULL_CARD_VALUE = -1

        self.seed()

        #self.reset()

    def _get_obs(self, player):
        list_obs = list()
        # first three values
        for card in player.hand:
            list_obs.append(card.abs_value)
        if len(player.hand)<self.HAND_SIZE:
            for i in range(self.HAND_SIZE-len(player.hand)):
                list_obs.append(self.NULL_CARD_VALUE)

        for card in self.playing_surface:
            list_obs.append(card.abs_value)
        if len(self.playing_surface)<self.MAX_PLAYING_SURFACE_SIZE:
            for i in range(self.MAX_PLAYING_SURFACE_SIZE-len(self.playing_surface)):
                list_obs.append(self.NULL_CARD_VALUE)

        return tuple(list_obs)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        random.seed(seed)
        return [seed]

    def init_game(self, n_players, human=False):
        '''
        Initialize a game, creating players, leaderboards, shuffling deck and init playing surface
        :param n_players: number of players of the game. Default is 2
        :param human: boolean signaling if human game must be set
        :return:
        '''
        for i in range(n_players-1):
            self.players.append(BasicAIPlayer(utils.generate_random_string()))
        if human:
            self.players.append(HumanPlayer('Human'))
        else:
            self.players.append(BasicAIPlayer(utils.generate_random_string()))

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

        # print "here I would check out the deck"

    def evolve(self, player, player_cards_selected):

        '''
            The function handles the action selected by player specified via
            the param player_cards_selected
            :param player, the player that is currently selecting cards
            :param player_cards_selected a list of selected cards, WITH HAND CARDS AT INDEX 0
            :return True if player take something
        '''
        obs = self._get_obs(player)
        print(obs)
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
        '''
        print the status of the game, playing surface and players hands
        :return:
        '''
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
        '''
        The function handles one turn. It deal cards and wait for all the player to complete their hand
        :return:
        '''

        print('Turn ', self.n_turns)

        self.deal_cards()

        if self.gui:
            self.renderer.render(self.playing_surface, self.players)
        self.print_status()

        # Wait for everyone to play. Append evolution result to evolution_history
        for k in range(self.HAND_SIZE):
            for i in range(self.n_players):
                player_cards_selected = self.players[i].act(self.playing_surface)
                if self.gui:
                    time.sleep(1)
                has_taken = self.evolve(self.players[i], player_cards_selected)
                self.evolution_history.append((self.players[i].name, has_taken))
                if self.gui:
                    self.renderer.render(self.playing_surface, self.players, i)

        self.n_turns += 1

    def compute_primiera(self, players):
        '''
        For all players apply primiera rules to compute their score
        :param players: list of players of the game
        :return: a dict with (k: player.name, value: primiera_score)
        '''

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
        '''
        Taking in input the given dictionary, the function updates overall leaderboard
        The functions checks for DRAW condition on given point. In the case, it does not update
        overall leaderboard
        :param dictionary: a dictionary with (k: player.name, value: a point score)
        :return:
        '''
        expected_value = next(iter(dictionary.values()))  # check for an empty dictionary first if that's possible
        all_equal = all(value == expected_value for value in dictionary.values())

        if not all_equal:
            self.leaderboard[max(zip(dictionary.values(), dictionary.keys()))[1]] += 1
        else:
            print(dictionary, " patta ")

    def compute_score(self):
        '''
        The function compute the overall score of the game computing denari, carte a lungo,
        setteoro e primiera and adding scope gained during game
        :return: the final leaderboard with (k: player.name, value: overall score)
        '''
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

        return self.leaderboard

    def start_game(self):
        '''
        The main loop of the game
        :return:
        '''

        while len(self.deck) != 0:
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
        print('Player status : ')
        for player in self.players:
            print(player.name)
            for card in player.gained_cards:
                print(card)

        self.compute_score()
        if self.gui:
            self.renderer.close_gui()

    '''
    def play(self):
        while True:
            CardEngine.update()
            CardEngine.render()
    '''

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