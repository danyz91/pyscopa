from cardgames.player import Player

class HumanPlayer(Player):

    def __init__(self, name):
        super().__init__(name)

    def let_user_pick(self, options):
        print("Please choose:")
        for idx, element in enumerate(options):
            print("{}) {}".format(idx + 1, element))
        i = input("Enter number: ")
        try:
            if 0 < int(i) <= len(options):
                return int(i)-1
        except:
            pass
        return None

    def act(self, playing_surface):
        all_takes = list()
        for card in self.hand:
            all_takes.extend(Player.get_possible_takes(card, playing_surface))

        take_strings = list()
        for take in all_takes:
            take_strings.append(str(take))

        selected_index = None
        while selected_index is None:
            selected_index = self.let_user_pick(take_strings)

        return all_takes[selected_index].get_all_cards()




