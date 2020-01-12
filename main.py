from cardgames.scopa import Scopa


def main():
    game = Scopa(gui=False)
    game.init_game(n_players=4, human=False)
    game.start_game()


if __name__ == '__main__':
    main()
