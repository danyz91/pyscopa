from cardgames.player import Player


class BasicAIPlayer(Player):

    def act(self, playing_surface):
        best_takes = list()
        for card in self.hand:
            best_takes.append(Player.get_max_take(card, playing_surface))

        best_take = max(best_takes)

        print('Player : ', self.name, ' choices to play ', best_take.played_card)

        if len(best_take.cards) == 0:
            print('no combination found')
        else:
            print(best_take)

        selected_cards_list = list()
        selected_cards_list.append(best_take.played_card)
        for card in best_take.cards:
            selected_cards_list.append(card)

        return selected_cards_list
