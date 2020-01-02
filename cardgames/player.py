from cardgames.card import Card
from cardgames import utils
from cardgames.take import Take
import random
import time



class Player:
    def __init__(self, name):
        self.name = name
        self.hand = list()
        self.gained_cards = list()
        self.pure_points = 0

    def inspect_card(self, card, playing_surface):
        score = 0
        at_least_one_pair = False
        possible_takes = list()

        for ps_card in playing_surface:
            if ps_card.value == card.value:
                curr_take = Take(card)
                curr_take.cards.append(ps_card)
                curr_take.evaluate_take(playing_surface)
                possible_takes.append(curr_take)
                at_least_one_pair = True

        comb_takes = list()
        if not at_least_one_pair:
            comb_takes = utils.subsets_with_sum(playing_surface, card.value)

        for take in comb_takes:
            curr_take = Take(card)
            for t_card in take:
                curr_take.cards.append(t_card)
            curr_take.evaluate_take(playing_surface)
            possible_takes.append(curr_take)

        if len(possible_takes) == 0:
            failed_take = Take(card)
            return failed_take

        #max_score_take = max(zip(take_dict.values(), take_dict.keys()))
        max_score_take = max(possible_takes)
        print('mx take', max_score_take)
        '''
        for el in max_score_take[0]:
            for card in playing_surface:
                if card.
        '''

        return max_score_take


    def act(self, playing_surface):
        '''
            :param playing_surface the status of the game
            :return a list of selected card, one in hand of player and the other (if present)
                    on the playing surface
        '''

        player_choice = random.choice(self.hand)

        best_takes = list()
        for card in self.hand:
            best_takes.append(self.inspect_card(card, playing_surface))

        best_take = max(best_takes)

        print('Player : ', self.name, ' choices to play ', best_take.played_card)

        if len(best_take.cards) == 0:
            print('no combination found')
        else:
            for card in best_take.cards:
                print(card)
        selected_cards_list = list()
        selected_cards_list.append(best_take.played_card)
        for card in best_take.cards:
            selected_cards_list.append(card)

        return selected_cards_list

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