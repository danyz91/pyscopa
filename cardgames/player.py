from cardgames import utils
from cardgames.take import Take

from abc import abstractmethod, ABC

class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.hand = list()
        self.gained_cards = list()
        self.pure_points = 0

    @staticmethod
    def get_possible_takes(card, playing_surface):
        '''
        The function returns a list of all possible takes for selected card given
        the status of playing surface
        :param card: the selected card
        :param playing_surface: the status of playing surface
        :return: a list of all possible takes
        '''
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
            possible_takes.append(failed_take)

        return possible_takes

    @staticmethod
    def get_max_take(card, playing_surface):
        '''
        The function return the best take between all possible takes for selected card
        taking into account current state of playing surface
        :param card: Selected card to be tested
        :param playing_surface: current status of playing surface
        :return: best take possible, an object containing card, playing surface cards and its score
        '''

        possible_takes = Player.get_possible_takes(card, playing_surface)

        max_score_take = max(possible_takes)

        return max_score_take

    @abstractmethod
    def act(self, playing_surface):
        '''
            :param playing_surface the status of the game
            :return a list of selected card, one in hand of player and the other (if present)
                    on the playing surface
        '''

        pass

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