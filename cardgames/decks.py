from cardgames.card import Card

decks = dict()
napolitan_deck = list()
french_deck= list()

for i in range(10):
    napolitan_deck.append(Card(i+1,'denari'))

for i in range(10):
    napolitan_deck.append(Card(i+1,'bastoni'))

for i in range(10):
    napolitan_deck.append(Card(i+1,'spade'))

for i in range(10):
    napolitan_deck.append(Card(i+1,'coppe'))



decks['napolitan'] = napolitan_deck