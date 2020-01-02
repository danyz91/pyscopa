suits_dict = {'denari' : 0,
              'bastoni': 1,
              'spade' : 2,
              'coppe' : 3}

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.abs_value = 10*suits_dict[self.suit]+self.value

    def __str__(self):
        card_string = str(self.value)+' '+self.suit
        out=''
        out+=' '+'-'*len(card_string)+'\n'
        out+='|'+card_string+'|'+'\n'
        out += ' ' + '-' * len(card_string)
        out += '\n'
        return out

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Card):
            return self.value == other.value and self.suit == other.suit

        return False