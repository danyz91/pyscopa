class Take:
    def __init__(self, player_card):
        self.played_card = player_card
        self.cards = list()
        self.score = 0

        self.SCOPA_SCORE = 20
        self.DENARI_SCORE = 1
        self.SETTE_SCORE = 1

    def evaluate_card(self, card):
        score = 0
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

    def __lt__(self, other):
        return self.score < other.score
