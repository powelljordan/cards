
'''
Areas are places where piles can be placed. Areas are created at the beginning of a game.
They are destroyed at the end of a game.
'''
from pile import Pile
from card import Card
class Area:
    def __init__(self, name="You should really name me", pile_location_list=[]):
        self.name = name
        self.pile_locations = {}
        for pile in pile_location_list:
            self.pile_locations[pile[0]] = pile[1]
        self.pile_count = len(pile_location_list)

    def __str__(self):
        self.check_rep()
        area_rep = "\n============================================"
        if self.pile_count == 0:
            area_rep = area_rep + "\nThere are no piles in "+self.name+"\n\n"
        if self.pile_count == 1:
            area_rep = area_rep + "\nThere is one pile in "+self.name+"\n\n"
        if self.pile_count > 1:
            area_rep = area_rep + "\nThere are "+str(self.pile_count)+" piles in "+self.name+"\n\n"
        for pile in self.pile_locations.keys():
            area_rep = area_rep + str(self.pile_locations[pile]) + "\n"

        return area_rep + "============================================\n\n"

    #Makes sure we're not losing piles anywhere
    def check_rep(self):
        assert self.pile_count == len(self.pile_locations.keys()), "I think this spot is actually a black hole and because piles are disappearing"
        assert self.pile_count >= 0, "I'm not sure how you did this, but there are a negative number of piles in this area"


    #Takes a tuple (location, pile) where location is a string that says where a pile is and pile is a Pile object
    #Adds the given pile to the specified area. If another pile exists there the old pile will become a part of the new pile so that
    #the top card of the resultant pile is the top card of the added pile
    def add_pile(self, new_pile_location):
        self.check_rep()
        desired_location, new_pile = new_pile_location
        if desired_location in self.pile_locations:
            present_value = self.pile_locations[desired_location]
            new_pile.add_pile(present_value)
            self.pile_locations[desired_location] = new_pile
        else:
            self.pile_locations[desired_location] = new_pile
            self.pile_count += 1



    #Removes a pile from this area. Returns the removed pile.
    def remove_pile(self, pile_location):
        self.check_rep()
        pile = self.pile_locations[pile_location]
        del self.pile_locations[pile_location]
        self.pile_count -= 1
        return pile

    #Returns all the pile locations defined in this area as a list
    def get_pile_locations(self):
        self.check_rep()
        return self.pile_locations.keys()

    #Returns the pile stored at a specific location in this area
    def get_pile(self, location):
        self.check_rep()
        return self.pile_locations[location]

#############################################################
#                          Tests                            #
#############################################################

SA = Card(style="bicycle", suit="spades", value="ace", face_up=True, color="black")
S2 = Card(style="bicycle", suit="spades", value="2", face_up=True, color="black")
S3 = Card(style="bicycle", suit="spades", value="3", face_up=True, color="black")

HA = Card(style="bicycle", suit="hearts", value="ace", face_up=True, color="red")
H2 = Card(style="bicycle", suit="hearts", value="2", face_up=True, color="red")
H3 = Card(style="bicycle", suit="hearts", value="3", face_up=True, color="red")

S4 = Card(style="bicycle", suit="spades", value="4", face_up=True, color="black")
S5 = Card(style="bicycle", suit="spades", value="5", face_up=True, color="black")

spades = Pile([SA, S2, S3])
hearts = Pile([H3, H2, HA])
communal_area = Area(name="communal area", pile_location_list = [("spades_location", spades), ("hearts_location", hearts)])
print communal_area
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nAdd 4 of spades to spades pile\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
communal_area.add_pile(("spades_location",Pile([S4])))
print communal_area
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nRemove hearts pile from communal area\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
communal_area.remove_pile("hearts_location")
print communal_area
stacking_area = Area("stacking area", pile_location_list = [("first_stack", Pile([S5]))])
print stacking_area
communal_area.add_pile(("spades_location",stacking_area.remove_pile("first_stack")))
# stacking_area.remove_pile("first_stack")
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nMoved 5 of spades form stacking area to communal area\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print stacking_area
print communal_area
