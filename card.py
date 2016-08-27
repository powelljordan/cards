'''
    The card class defines a basic playing card. The front and back of a card is specified in this class
'''
from types import BooleanType
class Card:
    def __init__(self, style=None, color=None, suit=None, value=None, face_up=False):
        self.face_up = face_up
        self.suit = suit
        self.color = color
        self.value = value
        self.style = style

    def __str__(self):
        self.check_rep()
        if self.face_up:
            return self.color+" "+self.value+" "+self.suit
        return "Style: "+self.style


    ## Makes sure that all card attributes have been defined and make sense for a valid card
    def check_rep(self):
        #Error strings
        card_attribute_error = "This card isn't quite right. One or more of its properties isn't defined"
        card_state_error = "This card isn't face up or face down. It must be balancing on the side"
        card_face_value_error = "This card is not valid. It'd be cool if it existed though."

        #Checks
        if self.suit == None:
            assert self.color == None, card_attribute_error
            assert self.value == None, card_attribute_error

        if self.color == None:
            assert self.suit == None, card_attribute_error
            assert self.value == None, card_attribute_error

        if self.value == None:
            assert self.suit == None, card_attribute_error
            assert self.color == None, card_attribute_error

        assert type(self.face_up) is BooleanType, card_state_error

        if self.suit.lower() == "diamonds":
            assert self.color.lower() == "red", card_face_value_error
        if self.suit.lower() == "hearts":
            assert self.color.lower() == "red", card_face_value_error
        if self.suit.lower() == "spades":
            assert self.color.lower() == "black", card_face_value_error
        if self.suit.lower() == "clubs":
            assert self.color.lower() == "black", card_face_value_error

    #Toggles a card between being face up pand ace down
    def flip_card(self):
        self.check_rep()
        if self.face_up:
            self.face_up = False
        else:
            self.face_up = True



#############################################################
#                          Tests                            #
#############################################################

ace_diamonds = Card(style="bicycle", suit="diamonds", value="ace", face_up=True, color="RED")
# print ace_diamonds
# ace_diamonds.flip_card()
# print ace_diamonds
# ace_diamonds.flip_card()
# print ace_diamonds
