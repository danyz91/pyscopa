from cardgames.player import Player


class BasicAIPlayer(Player):

    def act(self, playing_surface, verbose = False):
        best_takes = list()
        for card in self.hand:
            best_takes.append(Player.get_max_take(card, playing_surface))

        best_take = max(best_takes)

        if verbose:
            print('Player : ', self.name, ' choices to play ', best_take.played_card)

        if best_take.score < 0:
            if verbose:
                print('no combination -> penalty taken ', best_take.score)
        else:
            if verbose:
                print(best_take)

        selected_cards_list = list()
        selected_cards_list.append(best_take.played_card)
        for card in best_take.cards:
            selected_cards_list.append(card)

        return selected_cards_list
