from cardgames.card import Card
from cardgames import utils
import random


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = list()
        self.gained_cards = list()
        self.pure_points = 0


    def act(self, playing_surface):
        '''
            :param playing_surface the status of the game
            :return a list of selected card, one in hand of player and the other (if present)
                    on the playing surface
        '''
        cards_selected = list()
        player_choice = random.choice(self.hand)

        print('Player : ', self.name, ' choices to play ', player_choice)
        cards_selected.append(player_choice)

        pickup_choices = utils.subsets_with_sum(playing_surface, player_choice.value)

        if len(pickup_choices) == 0:
            return cards_selected

        final_choice = max(pickup_choices, key=len)

        card_choices = [curr_card for curr_card in playing_surface if
                        any(curr_card.value == x for x in final_choice)]

        for card in card_choices:
            cards_selected.append(card)

        return cards_selected

    def __str__(self):
        out=''
        out+='Player : '+self.name
        out+='\n'
        out+='Hand : '+'\n'
        for card in self.hand:
            out+=str(card)
        return out

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Player):
            return self.name == other.name