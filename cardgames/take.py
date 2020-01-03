class Take:
    def __init__(self, player_card):
        self.played_card = player_card
        self.cards = list()
        self.score = 0

        self.SCOPA_SCORE = 20
        self.DENARI_SCORE = 3
        self.SETTE_SCORE = 3

    def evaluate_card(self, card):
        score = 1
        if card.suit == 'denari':
            score += self.DENARI_SCORE
        if card.value == 7:
            score += self.SETTE_SCORE
        return score

    def evaluate_take(self, playing_surface):
        self.score = 0
        self.score += self.evaluate_card(self.played_card)

        for card in self.cards:
            self.score += self.evaluate_card(card)

        # scopa condition
        if len(self.cards) == len(playing_surface):
            self.score += self.SCOPA_SCORE

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
