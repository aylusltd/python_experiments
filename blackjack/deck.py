import random
import constants

def makeCard(seed):
    card = {}
    card["value"] = min(((seed+1) % 13),10)
    # edge case for kings
    if card["value"] == 0:
        card["value"] = 10
    card["name"] = constants.Names[seed % 13]
    card["suit"] = constants.Suits[seed/13]
    card["display"] = constants.D[seed%13]
    return card

class Deck(list):
    current_card=0
    def __init__(self, *args, **kwargs):
        super(Deck, self)
        for i in range(0,51):
            self.append(makeCard(i))
        random.shuffle(self)
    def deal(self):
        self.current_card+=1
        return self[self.current_card-1]
    def shuffle(self):
        random.shuffle(self)
        self.current_card=0        

        