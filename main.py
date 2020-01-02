from cardgames.scopa import Scopa


def main():
    '''
    print('Init Scopa')
    scopa_game = Scopa()
    scopa_game.init_game(n_players=2)
    print(scopa_game)

    scopa_game.start_game()
    '''
    game = Scopa(gui=True)
    game.init_game(n_players=2)
    #game.check_out_deck()
    game.start_game()

if __name__ == '__main__':
    main()
