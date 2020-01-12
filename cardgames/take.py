from cardgames.utils import NULL_CARD_VALUE

class Take:
    def __init__(self, player_card):
        self.played_card = player_card
        self.cards = list()
        self.score = 0

        self.SCOPA_SCORE = 20
        self.DENARI_SCORE = 3
        self.SETTE_SCORE = 5
        self.POTENTIAL_PURE_POINT_PENALTY = 10

        self.TAKE_MAX_LEN = 5

    def evaluate_card(self, card):
        score = 1
        if card.suit == 'denari':
            score += self.DENARI_SCORE
        if card.value == 7:
            score += self.SETTE_SCORE
        return score

    def evaluate_take(self, playing_surface):
        self.score = 0

        if len(self.cards) != 0:
            self.score += self.evaluate_card(self.played_card)

            for card in self.cards:
                self.score += self.evaluate_card(card)

            # scopa condition
            if len(self.cards) == len(playing_surface):
                self.score += self.SCOPA_SCORE
        else:
            self.score += -self.evaluate_card(self.played_card)
            surface_sum = sum(card.value for card in playing_surface)
            if self.played_card.value <= 10-surface_sum:
                self.score += -self.POTENTIAL_PURE_POINT_PENALTY

        return self.score

    def sum_take(self):
        sum_t = 0
        for card in self.cards:
            sum_t += self.evaluate_card(card)
        return sum_t

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        out = ''
        out += 'Player card : '+str(self.played_card)
        out += '\tCards : '
        for card in self.cards:
            out += str(card)
        out += '\tScore : '+str(self.score)

        return out

    def get_all_cards(self):
        ret = list()
        ret.append(self.played_card)
        ret.extend(self.cards)

        return ret

    def get_take_as_tuple(self):
        take_list = self.get_all_cards()
        take_abs_list = [card.abs_value for card in take_list]
        take_abs_list += [NULL_CARD_VALUE] * (self.TAKE_MAX_LEN - len(take_list))
        tuple(take_list)
