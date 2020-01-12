from cardgames.scopa import Scopa
import argparse

parser = argparse.ArgumentParser(description='PyScopa launcher')

parser.add_argument('-g', '--gui', help='Enable gui', action='store_true')
parser.add_argument('-p', '--human', help='Enable Human player', action='store_true')
parser.add_argument('-n', '--n_players', type=int, help='Number of players', default=2, choices=(2, 3, 4))


def main():
    args = parser.parse_args()
    game = Scopa(gui=args.gui)
    game.init_game(n_players=args.n_players, human=args.human)
    game.start_game()


if __name__ == '__main__':
    main()
