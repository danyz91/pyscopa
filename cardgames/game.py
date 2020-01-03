####

import os
import time


from guizero import App, Picture

####
CARD_WIDTH = 102
CARD_HEIGHT = 162
FIRST_PLAYER_ROW = 0
PLAYING_SURFACE_ROW = 2
SECOND_PLAYER_ROW = 4
GREEN_BACKGROUND = (53,181,117)

class ImageCard(object):
    def __init__(self, card, image):
        self.card = card
        self.image = image

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, ImageCard):
            return self.card == other.card

        return False


class GameRenderer(object):

    def __init__(self, deck, width=1024, height=640, res_folder="res", img_folder="img"):

        self.width = width
        self.height = height

        self.app = App(layout="grid", title="PyScopa GUI", bg=GREEN_BACKGROUND,
                       width=self.width, height=self.height)

        self.deck = deck.copy()
        # load all card image
        self.imaged_deck = list()
        self.img_folder = os.path.join(res_folder, img_folder)
        self.base_folder = "cardgames"
        for card in self.deck:
            curr_img_path = os.path.join(self.base_folder, self.img_folder, card.suit, str(card.value))+'.gif'
            self.imaged_deck.append(ImageCard(card, curr_img_path))

        self.back_card_path = os.path.join(self.base_folder, self.img_folder, 'card_back')+'.gif'
        self.images = list()

    def render(self, first_player_hand, playing_surface, second_player_hand):

        for image in self.images:
            image.destroy()

        self.images.clear()
        # first player hand
        col_index = 0
        self.images.append(Picture(self.app, image=self.back_card_path , grid=[col_index, FIRST_PLAYER_ROW], width=CARD_WIDTH,
                          height=CARD_HEIGHT))
        col_index += 1

        for card in first_player_hand:
            curr_img_path = self.imaged_deck[self.deck.index(card)].image
            self.images.append(Picture(self.app, image=curr_img_path, grid=[col_index, FIRST_PLAYER_ROW], width=CARD_WIDTH,
                          height=CARD_HEIGHT))

            col_index+=1

        # PLAYING SURFACE
        col_index = 0
        self.images.append(
            Picture(self.app, image=self.back_card_path, grid=[col_index, PLAYING_SURFACE_ROW], width=CARD_WIDTH,
                    height=CARD_HEIGHT))
        col_index += 1

        for card in playing_surface:
            curr_img_path = self.imaged_deck[self.deck.index(card)].image
            self.images.append(Picture(self.app, image=curr_img_path, grid=[col_index, PLAYING_SURFACE_ROW], width=CARD_WIDTH,
                               height=CARD_HEIGHT))
            col_index += 1

        # second player hand
        col_index = 0
        self.images.append(
            Picture(self.app, image=self.back_card_path, grid=[col_index, SECOND_PLAYER_ROW], width=CARD_WIDTH,
                    height=CARD_HEIGHT))
        col_index += 1

        for card in second_player_hand:
            curr_img_path = self.imaged_deck[self.deck.index(card)].image
            self.images.append(Picture(self.app, image=curr_img_path, grid=[col_index, SECOND_PLAYER_ROW], width=CARD_WIDTH,
                               height=CARD_HEIGHT))

            col_index += 1

        self.app.update()
        time.sleep(1)
        #input()

    def close_gui(self):
        print('close gui')
        #self.app.close()

