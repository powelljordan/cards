'''
A first attempt at making a game. Nertz should be a reasonably complex first game to hopefully
hit as many edge cases as possible.
'''
from card import Card
from pile import Pile
from area import Area
import random
class Nertz:
    def __init__(self, players=[], adjusting_nertz_pile=False):
        self.players = players
        self.adjusting_nertz_pile = adjusting_nertz_pile
        self.player_areas = self.generatePlayerAreas(players)
        self.turn = 0
        self.nertz_pile_count = 13

    #Return visible game state
    def __str__(self):
        game_state = ""
        for player in self.player_areas:
            if player != "communal_area":
                for area in self.player_areas[player]:
                    game_state = "\n" + game_state + player + "'s " + str(area) + str(self.player_areas[player][area])
        game_state = game_state + str(self.player_areas["communal_area"])
        return game_state

    #Generates the necessary areas for each player_areas
    def generatePlayerAreas(self, players):
        player_areas = {}
        #Create the three areas each player has. A nertz area with space for one pile.
        #A stacking area with space for 4 piles. A hand area that consists of two piles, one
        #represents the three cards that are face up from which the user can select the top card
        #and one that has the remaining face down cards
        for player in players:
            nertz_pile_area = Area("nertz_pile_area", [])
            stacking_area = Area("stacking_area", [])
            flipping_area = Area("flipping_area", [])
            player_areas[player] = {"nertz_pile_area": nertz_pile_area, "stacking_area":stacking_area, "flipping_area":flipping_area}
        communal_area = Area("communal_area", [])
        player_areas["communal_area"] = communal_area
        return player_areas


    def deal_cards(self):
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        suit_color = [("hearts", "red"), ("diamonds", "red"), ("spades", "black"), ("clubs", "black")]
        for player in players:
            self.turn += 1
            #Create a deck of 52 cards
            standard_deck = Pile([Card(style=player,color=color, suit=suit, value=val) for val in values for (suit, color) in suit_color])
            #shuffle that deck a random number of times
            standard_deck.shuffle(3+self.turn) #changed this just for testing
            #take off the top 13 cards
            nertz_pile_area_cards = Pile()
            for i in range(self.nertz_pile_count - 1):
                nertz_pile_area_cards.add_card(standard_deck.draw_card())
            #flip over the 13th card
            flipped_top_card = standard_deck.draw_card()
            flipped_top_card.flip_card()
            nertz_pile_area_cards.add_card(flipped_top_card)
            #put those cards in the nertz pile area
            self.player_areas[player]["nertz_pile_area"].add_pile(("nertz_pile_location", nertz_pile_area_cards))
            #shuffle the deck a random number of times
            # standard_deck.shuffle(random.randint(3, 6)) #changed this just for testing
            standard_deck.shuffle(3+self.turn)
            #put one card in each stacking pile within the stacking area
            stacking_locations = ["first", "second", "third", "fourth"]
            for location in stacking_locations:
                top_card = standard_deck.draw_card()
                top_card.flip_card()
                top_card_pile = Pile([top_card])
                self.player_areas[player]["stacking_area"].add_pile((location, top_card_pile))
            #put the rest in the flipping_area
            self.player_areas[player]["flipping_area"].add_pile(("flipping_location", standard_deck))
        #This bit here goes through and prints out everything for visual verification


    def move(self, from_area, from_pile_location, to_area, to_pile_location, player=None, flip=False):
        if player is None:
            player = self.players[0]
        #Check the rules that this is a valid move
        if self.rules(from_area, to_area):
            #The communal_area isn't based on a player and so it's at the player level of the dictionary
            if from_area == "communal_area":
                card = self.player_areas[from_area].get_pile(from_pile_location).draw_card()
                card_at_dest = self.player_areas[player][to_area].pile(to_pile_location).view_top_card()
                destination = self.player_areas[player][to_area].pile(to_pile_location)

            elif to_area == "communal_area":
                card = self.player_areas[player][from_area].get_pile(from_pile_location).draw_card()
                card_at_dest = self.player_areas[to_area].get_pile(to_pile_location).view_top_card()
                destination = self.player_areas[to_area].get_pile(to_pile_location)
            #If it's not in the communal area then we need to get look at a specific player's playing areas
            else:
                card = self.player_areas[player][from_area].get_pile(from_pile_location).draw_card()
                card_at_dest = self.player_areas[player][to_area].pile(to_pile_location).view_top_card()
                destination = self.player_areas[player][to_area].pile(to_pile_location)
            if flip:
                card.flip_card()
            destination.add_card(card)

    def flip_cards(self, player=None, num_to_flip=3):
        area = "flipping_area"
        from_location = "flipping_location"
        to_location = "playing_location"
        if player is None:
            player = self.player[0]
        if self.player_areas[player][area].get_pile(from_location).card_count > 0:
            for i in range(num_to_flip):
                self.move(area, from_location, area, to_location, player, True)
            return self.player_areas[player][area].get_pile(to_location).view_top_card()
        return None

    def rules(self, from_area, to_area):
        return True






players = ["jordan", "annie"]
nertz_test = Nertz(["jordan", "annie"])
print nertz_test
nertz_test.deal_cards()
print nertz_test
nertz_test.move("stacking_area", "fourth", "communal_area", "annie_spades", "annie")
print nertz_test
nertz_test.move("flipping_area")
