####

import os
import time

from guizero import App, Picture, Box, Text

####
CARD_WIDTH = 116
CARD_HEIGHT = 179
FIRST_PLAYER_ROW = 0
PLAYING_SURFACE_ROW = 2
SECOND_PLAYER_ROW = 4
THIRD_PLAYER_COL = 0
FOURTH_PLAYER_COL = 10
GREEN_BACKGROUND = (53, 181, 117)

#CARD_WIDTH = int(CARD_WIDTH*3/4)
#CARD_HEIGHT = int(CARD_HEIGHT*3/4)


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

    def __init__(self, deck, players, width=1024, height=768, res_folder="res", img_folder="img"):

        self.width = width
        self.height = height

        # Graphical elements
        self.app = App(layout="auto", title="PyScopa GUI", bg=GREEN_BACKGROUND,
                       width=self.width, height=self.height)
        self.first_player_box = Box(self.app, width="fill", align="top", border=True, height=CARD_HEIGHT+10)
        self.second_player_box = Box(self.app, width="fill", align="bottom", border=True, height=CARD_HEIGHT+10)
        self.third_player_box = Box(self.app, height="fill", align="left", border=True, width=CARD_WIDTH)
        self.fourth_player_box = Box(self.app, height="fill", align="right", border=True, width=CARD_WIDTH)
        self.playing_surface_box = Box(self.app, width="fill", border=True, height=2*CARD_HEIGHT)

        self.first_player_name = Text(self.first_player_box, text=players[0].name)
        self.second_player_name = Text(self.second_player_box, text=players[1].name)
        if len(players) > 2:
            self.third_player_name = Text(self.third_player_box, text=players[2].name)
            if len(players) > 3:
                self.fourth_player_name = Text(self.fourth_player_box, text=players[3].name)
            else:
                self.fourth_player_name = Text(self.fourth_player_box, text="player 4")
        else:
            self.third_player_name = Text(self.third_player_box, text="player 3")

        self.playing_surface_name = Text(self.playing_surface_box, text="surface")

        # Deck, cards elements and Image loading
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

    def render(self, playing_surface, players, turn=None):

        first_player_hand = players[0].hand
        second_player_hand = players[1].hand
        third_player_hand = None
        fourth_player_hand = None
        if len(players) > 2:
            third_player_hand = players[2].hand
            if len(players) > 3:
                fourth_player_hand = players[3].hand

        for image in self.images:
            image.destroy()

        self.images.clear()

        self.first_player_name.text_color = "black"
        self.second_player_name.text_color = "black"
        self.third_player_name.text_color = "black"
        self.fourth_player_name.text_color = "black"

        if turn == 0:
            self.first_player_name.text_color = "red"
        elif turn == 1:
            self.second_player_name.text_color = "red"
        elif turn == 2:
            self.third_player_name.text_color = "red"
        elif turn == 3:
            self.fourth_player_name.text_color = "red"

        # first player hand
        for card in first_player_hand:
            curr_img_path = self.imaged_deck[self.deck.index(card)].image
            self.images.append(Picture(self.first_player_box, image=curr_img_path,
                                       width=CARD_WIDTH, height=CARD_HEIGHT, align="left"))

        # PLAYING SURFACE
        for card in playing_surface:
            curr_img_path = self.imaged_deck[self.deck.index(card)].image
            self.images.append(Picture(self.playing_surface_box, image=curr_img_path,
                                       width=CARD_WIDTH, height=CARD_HEIGHT, align="left"))

        # second player hand
        for card in second_player_hand:
            curr_img_path = self.imaged_deck[self.deck.index(card)].image
            self.images.append(Picture(self.second_player_box, image=curr_img_path,
                                       width=CARD_WIDTH, height=CARD_HEIGHT,  align="left"))

        if third_player_hand is not None:
            # third player hand
            for card in third_player_hand:
                curr_img_path = self.imaged_deck[self.deck.index(card)].image
                self.images.append(
                    Picture(self.third_player_box, image=curr_img_path, width=CARD_WIDTH, height=CARD_HEIGHT))

        if fourth_player_hand is not None:
            # fourth player hand
            for card in fourth_player_hand:
                curr_img_path = self.imaged_deck[self.deck.index(card)].image
                self.images.append(
                    Picture(self.fourth_player_box, image=curr_img_path, width=CARD_WIDTH, height=CARD_HEIGHT))

        self.app.update()
        time.sleep(1)

    def close_gui(self):
        print('close gui')
        #self.app.close()

