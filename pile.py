from types import ListType
from card import Card
from itertools import islice, cycle
import random

class Pile:
    def __init__(self, card_list=[]):
        self.card_list = card_list
        self.card_count = len(card_list)

    def __str__(self):
        self.check_rep()
        card_count_info = ""
        card_list_info = ""
        if self.card_count == 0:
            card_count_info = card_count_info + "There are no cards in this pile. "
        if self.card_count == 1:
            card_count_info = card_count_info + "There is 1 card in this pile. "
            card_list_info = "The top card is a "+ str(self.card_list[0]) + "\n"
        if self.card_count > 1:
            card_count_info = card_count_info + "There are "+str(self.card_count)+" cards in this pile. "
            card_list_info = "The top card is a "+ str(self.card_list[0]) + "\n"
        # for card in self.card_list:
        #     card_list_info = card_list_info + str(card) + "\n"

        card_count_info = card_count_info + "\n" + card_list_info

        return card_count_info

    def __len__(self):
        self.check_rep()
        return self.card_count

    #Makes sure that pile parameters mkae sense
    def check_rep(self):
        #Error strings
        pile_count_error = "There are a negative number cards. Check under the table, maybe they fell"
        pile_list_error = "This pile doesn't have a list of cards."
        pile_card_error = "The card count "+str(self.card_count)+" isn't quite right by my count "+str(len(self.card_list))+" . Is that an contraband ace you're slipping in?"

        #Checks
        assert self.card_count >= 0, pile_count_error
        assert len(self.card_list) == self.card_count, pile_card_error

    def view_top_card(self):
        self.check_rep()
        if self.card_count > 0:
            return self.card_list[0]
        return None

    def get_all_cards(self):
        self.check_rep()
        return self.card_list

    #Adds a single card to a pile
    def add_card(self, card):
        self.check_rep()
        self.card_list = [card] + self.card_list
        self.card_count += 1

    #Adds all the cards in another pile to this pile
    def add_pile(self, pile):
        self.check_rep()
        self.card_list.extend(pile.card_list)
        self.card_count += pile.card_count


    #Removes a card from the top of this pile and returns that card
    def draw_card(self):
        self.check_rep()
        if self.card_count > 0:
            self.card_count -= 1
            return self.card_list.pop(0)
        return None

    #Removes a pile from the top of this pile and returns that pile
    def remove_pile(self, pile_size):
        self.check_rep()
        if pile_size > self.card_count:
            pile_size = card_count
        new_pile_list = self.card_list[0:pile_size]
        self.card_list = self.card_list[pile_size:]
        self.card_count -= pile_size
        return Pile(new_pile_list)

    #Cuts this pile into the desired number of piles and returns a list of all the piles
    def cut(self, number_of_piles):
        self.check_rep()
        number_of_cards = self.card_count
        number_of_cards_in_subpile = number_of_cards/number_of_piles
        new_pile_list = []
        extra_cards = number_of_cards % number_of_piles
        for i in range(number_of_piles - 1):
            new_pile_list.append(self.remove_pile(number_of_cards_in_subpile))
        new_pile_list = [self] + new_pile_list
        return new_pile_list

    def roundrobin(self, *iterables):
        "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
        # Recipe credited to George Sakkis
        pending = len(iterables)
        nexts = cycle(iter(it).next for it in iterables)
        while pending:
            try:
                for next in nexts:
                    yield next()
            except StopIteration:
                pending -= 1
                nexts = cycle(islice(nexts, pending))

    def shuffle(self, number_of_times):
        self.check_rep()
        combined_hand = self.card_list
        for i in range(number_of_times):
            mid = len(combined_hand)/2
            left_hand = combined_hand[:mid]
            right_hand = combined_hand[mid:]
            combined_hand = list(self.roundrobin(left_hand, right_hand))
        self.card_list = combined_hand
        return self

# Flips every card in the deck (I think it works. . .)
    def flipDeck(self):
        for card in self.card_list:
            card.flip_card()
        return None

def generateDeck(card_values, card_suit_color_map):
    final_deck = Pile()
    for value in card_values:
        for key in card_suit_color_map:
            final_deck.add_card(Card(style="bicycle", suit=key, value=value, color=card_suit_color_map[key], face_up=True))
    return final_deck


#############################################################
#                          Tests                            #
#############################################################

# deck = generateDeck(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"], {"hearts":"red", "diamonds": "red", "spades":"black", "clubs":"black"})

def reset():
    deck = generateDeck(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"], {"hearts":"red", "diamonds": "red", "spades":"black", "clubs":"black"})



ace_diamonds = Card(style="bicycle", suit="diamonds", value="ace", face_up=True, color="RED")
nertz_pile = Pile(card_list=[ace_diamonds])
#print deck
# decks = deck.cut(3)
# print decks
# for deck in decks:
#     print deck
# print nertz_pile
# for i in range(8):
#     print deck.shuffle(1)
# print deck.flipDeck()
