class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        out=''
        out+=str(self.value)+' '+self.suit
        out += '\n'
        return out

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Card):
            return self.value == other.value and self.suit == other.suit

        return False