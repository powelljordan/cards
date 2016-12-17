'''
A first attempt at making a game. Nertz should be a reasonably complex first game to hopefully
hit as many edge cases as possible.
'''
from card import Card
from pile import Pile
from area import Area
import random
import datetime
import time
import re
class Nertz:
    def __init__(self, players=[], adjusting_nertz_pile=False, log_name=None):
        self.players = players
        self.adjusting_nertz_pile = adjusting_nertz_pile
        self.player_areas = self.generatePlayerAreas(players)
        self.turn = 0
        self.nertz_pile_count = 13
        self.log_name = log_name
        welcome = "Let's play Nertz"
        for player_index in range(len(players)):
            if player_index < len(players) - 1:
                welcome = welcome + ", "+players[player_index]
            else:
                welcome = welcome + " and "+players[player_index]+"!"
        self.log(welcome)
        print welcome
        self.user_input()

    #Return visible game state
    def __str__(self):
        game_state = ""
        for player in self.player_areas:
            if player in self.players:
                game_state = game_state + "###########################################\n"
            if player != "communal_area":
                for area in self.player_areas[player]:
                    game_state = "\n" + game_state + player + "'s " + str(area) + str(self.player_areas[player][area])
            if player in self.players:
                game_state = game_state + "###########################################\n\n\n\n\n"

        game_state = game_state + str(self.player_areas["communal_area"])
        output = game_state
        self.log(output)
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
        self.log("Dealing Cards . . . ")
        for player in players:
            self.turn += 1
            #Create a deck of 52 cards
            standard_deck = Pile([Card(style=player,color=color, suit=suit, value=val) for val in values for (suit, color) in suit_color])
            #shuffle that deck a random number of times
            standard_deck.shuffle(4+self.turn) #changed this just for testing
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
        self.log("Cards Dealt" + str(self))
        #This bit here goes through and prints out everything for visual verification


    def move(self, from_area, from_pile_location, to_area, to_pile_location, player=None, flip=False, log=True):
        flipping_area = "flipping_area"
        if player is None:
            player = self.players[0]
        #Check the rules that this is a valid move
        if self.rules(from_area, from_pile_location, to_area, to_pile_location, player):
            #The communal_area isn't based on a player and so it's at the player level of the dictionary

            if to_area == "communal_area":
                card = self.player_areas[player][from_area].get_pile(from_pile_location).draw_card()
                pile_at_dest = self.player_areas[to_area].get_pile(to_pile_location)
                if pile_at_dest != None:
                    card_at_dest = pile_at_dest.view_top_card()
                    if card.value == "K":
                        card.flip_card()

                else:
                    card_at_dest = None
                    self.player_areas[to_area].add_pile((to_pile_location, Pile([])))
                    pile_at_dest = self.player_areas[to_area].get_pile(to_pile_location)

            #If it's not in the communal area then we need to get look at a specific player's playing areas
            else:
                card = self.player_areas[player][from_area].get_pile(from_pile_location).draw_card()
                pile_at_dest = self.player_areas[player][to_area].get_pile(to_pile_location)
                if pile_at_dest != None:
                    card_at_dest = pile_at_dest.view_top_card()
                else:
                    card_at_dest = None
                    #The flipping and communal areas are the only two that should have a variable number of piles
                    #As a result this little add pile logic only exists for those two. The number of stacking area
                    #and nertz area piles are fixed and should not change at any point during the game even if one is empty
                    if to_area == flipping_area:
                        self.player_areas[player][to_area].add_pile((to_pile_location, Pile([])))
                        pile_at_dest = self.player_areas[player][to_area].get_pile(to_pile_location)
                if from_area == "nertz_pile_area":
                    self.flip(from_area, from_pile_location, player=player)
            if flip:
                card.flip_card()
            pile_at_dest.add_card(card)

            if log:
                if to_area == "communal_area":
                    self.log(str(card) + " was moved from " +player+"'s " + from_area + " to "+ to_area)
                    self.log(str(self.player_areas[player][from_area]))
                    self.log(str(self.player_areas[to_area]))

                else:
                    if to_area == from_area:
                        self.log(str(card) + " was moved from " +player+"'s "+ from_pile_location + " to "+player+"'s " + to_pile_location)
                        self.log(str(self.player_areas[player][to_area]))
                    else:
                        self.log(str(card) + " was moved from "+player+"'s " + from_area + " to " +player+"'s "+ to_area)
                        self.log(str(self.player_areas[player][from_area]))
                        self.log(str(self.player_areas[player][to_area]))

    def flip_cards(self, player=None, num_to_flip=3):
        area = "flipping_area"
        from_location = "flipping_location"
        to_location = "playing_location"
        count = 0
        if player is None:
            player = self.players[0]
        if self.player_areas[player][area].get_pile(from_location).card_count > 0:
            for i in range(num_to_flip):
                if self.player_areas[player][area].get_pile(from_location).card_count > 0:
                    count += 1
                    if count == num_to_flip:
                        self.log(str(count) + " cards were flipped in "+player+"'s "+"flipping area.")
                        self.move(area, from_location, area, to_location, player, True, True)
                    else:
                        self.move(area, from_location, area, to_location, player, True, False)
                else:
                    pile = self.player_areas[player][area].get_pile(to_location)
                    card_list = [card for card in self.player_areas[player][area].get_pile(to_location).card_list]
                    for e in card_list:
                        self.move(area, to_location, area, from_location, player, True, True)
            # print len(self.player_areas[player][area].get_pile(to_location).card_list)
            return self.player_areas[player][area].get_pile(to_location).view_top_card()
        # print self.player_areas[player][area].get_pile(from_location).card_count
        return None

    def flip(self, area, location, player=None):
        if player is None:
            player = self.players[0]
        try:
            pile = self.player_areas[player][area].get_pile(location)
            card = pile.view_top_card()
            pile.draw_card()
            card.flip_card()
            pile.add_card(card)
        except AttributeError as e:
            print e


    def rules(self, from_area, from_pile_location, to_area, to_pile_location, player):
        ##Value Map
        value_map = {"A": 1, \
                     "2": 2, \
                     "3": 3, \
                     "4": 4, \
                     "5": 5, \
                     "6": 6, \
                     "7": 7, \
                     "8": 8, \
                     "9": 9, \
                     "10":10, \
                     "J": 11, \
                     "Q": 12, \
                     "K": 13, \
                    }

        ## Nertz Pile rules
        if to_area == "nertz_pile_area":
            print "Cards cannot be added to the Nertz pile"
            return False

        ## Flipping Area rules
        if to_area == "flipping_area" :
            if from_area == "flipping_area":
                return True
            print "Cards cannot be added to the flipping area"
            return False

        ## Communal Area rules
        if from_area == "communal_area":
            print "Cards cannot be taken from the communal area"
            return False

        if to_area == "communal_area":
            origin_pile = self.player_areas[player][from_area].get_pile(from_pile_location)
            destination_pile = self.player_areas[to_area].get_pile(to_pile_location)
            if origin_pile == None:
                print "There are no cards in the pile you're looking at"
                return False

            if destination_pile:
                if value_map[origin_pile.view_top_card().value] == value_map[destination_pile.view_top_card().value] + 1 and\
                    origin_pile.view_top_card().suit == destination_pile.view_top_card().suit:
                    return True
                else:
                    print "You can't play a "+str(origin_pile.view_top_card())+" on top of a "+str(destination_pile.view_top_card())
                    return False

            if destination_pile == None and origin_pile.view_top_card().value == "A":
                return True

            if destination_pile == None:
                print "You can only move Aces to empty piles. You tried to move a " + str(origin_pile.view_top_card())
                return False
        ## Stacking Area rules
        # print "EY THERE", self.player_areas[player][from_area].get_pile(from_pile_location), "done"
        origin_pile = self.player_areas[player][from_area].get_pile(from_pile_location)
        # print origin_pile.view_top_card().value
        destination_pile = self.player_areas[player][to_area].get_pile(to_pile_location)
        # print self.player_areas[player][to_area]

        if to_area == "stacking_area":
            try:
                if value_map[origin_pile.view_top_card().value] == value_map[destination_pile.view_top_card().value] - 1 and\
                    origin_pile.view_top_card().color != destination_pile.view_top_card().color:
                    return True
                else:
                    print "You can't play a "+str(origin_pile.view_top_card())+" on top of a "+str(destination_pile.view_top_card())
                    return False
            except AttributeError:
                if origin_pile.view_top_card() == None:
                    print str(origin_pile)
                    return False
                elif destination_pile.view_top_card() == None:
                    return True

        return True

    #Creates a file where events that happen during a game of nertz are stored
    #If no name is is specified the game is logged to a file named with the time stamp when the game is initiated
    def log(self, output, name=None):
        name = self.log_name
        if name:
            with open("c:/Users/Jordan/Documents/cards/" + name + ".txt", 'a+') as nertz_game_log:
                nertz_game_log.write(output + "\n\n")
        else:
            with open("c:/Users/Jordan/Documents/cards/"+str(strftime("%Y-%m-%d %H:%M:%S")) + ".txt", 'a+') as nertz_game_log:
                nertz_game_log.write(output)


    def user_input(self):
        dealt = False
        cmd = raw_input("nertz_prompt# ")
        self.log("nertz_prompt# "+cmd)
        args = re.split("\s+", cmd)
        if args[0] == "show":
            if len(args) == 1:
                print self
            elif len(args) == 2:
                if args[1] in self.players:
                    for area in self.player_areas[args[1]]:
                        print area
                elif args[1] == "players":
                    for player in players:
                        print player
                elif args[1] == "communal_area":
                    print self.player_areas[args[1]]
                else:
                    print "Sorry "+args[1]+" is not a player currently in the game. "+args[1]+" can join next game."
            elif len(args) == 3:
                if args[1] in self.players:
                    if args[2] in self.player_areas[args[1]]:
                        print self.player_areas[args[1]][args[2]]
                    elif args[2] == "areas":
                        for area in self.player_areas[args[1]]:
                            print area
                    else:
                        print "There's no "+args[1]+" area. I suppose we could consider making one for this game"
                else:
                    print "Sorry "+args[1]+" is not a player currently in the game. "+args[1]+" can join next game."
            elif len(args) == 4:
                if args[1] in self.players:
                    if args[2] in self.player_areas:
                        if args[3] in self.player_areas[args[1]][args[2]].get_pile_locations():
                            print self.player_areas[args[1]][args[2]].get_pile([args[3]])
                        elif args[3] == "piles":
                            for pile in self.player_areas[args[1]][args[2]].get_pile_locations():
                                print pile
                        else:
                            print "There's no "+args[3]+" pile in "+args[2]
                    else:
                        print "There's no "+args[1]+" area. I suppose we could consider making one for this game"
                else:
                    "Sorry "+args[1]+" is not a player currently in the game. "+args[1]+" can join next game."
            self.user_input()

        elif args[0] == "deal":
            if dealt:
                print "You've already dealt cards"
            else:
                self.deal_cards()
                print "Dealing ..."
                time.sleep(1)
                print self
            self.user_input()

        elif args[0] == "move":
            args = cmd.split(" ")
            if len(args) < 5:
                print "Please specify at least 4 arguments:\n origin_area[string], origin_pile_location_within_area[string], destination_area[string], destination_pile_location_within_area[string]\n"
                print "For example: move [stacking_area] [first] [communal_area] [annie_spades]"
                print "Additionally you can specify player[string]"

            elif len(args)> 6:
                print "Please specify at most 6 arguments:\n origin_area[string], origin_pile_location_within_area[string], destination_area[string],\
                 destination_pile_location_within_area[string]  player[string]\n"
                print "For example: move [stacking_area] [first] [communal_area] [annie_spades] [annie]"
                print "You entered: "+str(args)

            elif len(args) == 5:
                self.move(args[1], args[2], args[3], args[4])

            elif len(args) == 6:
                if args[5] in self.players:
                    self.move(args[1], args[2], args[3], args[4], args[5])
                else:
                    print "Sorry "+args[5]+" is not a player currently in the game. "+args[5]+" can join next game."

            self.user_input()
        elif args[0] == "flip":
            args=cmd.split()
            try:
                if len(args) > 1:
                    self.flip_cards(args[1])
                else:
                    self.flip_cards()
            except IndexError:
                pass
            self.user_input()


        elif args[0] == "help":
            print "\nAvailable commands are 'show', 'deal', and 'move'\n"
            print "'show' takes up to two optional arguments to show you a specific area or pile. Usage: show [player] [area] [pile]\n"
            print "'deal' Deals the cards for a standard nertz game then shows you where they are.\n"
            print "'move' Allows you to move a card from one pile to another in accordance with the rules of Nertz. \n Usage: move, origin area, origin pile location, desitination area, destination pile location, [player]\n"
            self.user_input()

        elif args[0] == "exit":
            return

        else:
            print "Not a valid command. Type 'help' for a list of commands"
            self.user_input()














players = ["jordan", "annie"]
nertz_test = Nertz(["jordan", "annie"], log_name="nertz_log_2")
# print nertz_test
# nertz_test.deal_cards()
# print nertz_test
# nertz_test.move("stacking_area", "first", "communal_area", "annie_spades", "annie")
# print nertz_test
# nertz_test.move("nertz_pile_area", "nertz_pile_location", "stacking_area", "first", "annie")
# # nertz_test.flip_cards("jordan")
# print nertz_test
# nertz_test.flip_cards("jordan")
# print nertz_test
