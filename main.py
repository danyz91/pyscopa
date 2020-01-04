from cardgames.scopa import Scopa


def main():
    game = Scopa(gui=True)
    game.init_game(n_players=3, human=False)
    game.start_game()

if __name__ == '__main__':
    main()
