Names = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
D = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
Suits = [u'\u2665', u'\u2666', u'\u2663', u'\u2660']
min_bet = 1
starting_bank = 100
black_jack_multiplier = 1.5

endings = ["th", "st", "nd", "rd"]
endings_cutoff = 20

def get_ending(n):
    n = n%100
    if n>endings_cutoff:
        n=n%10
    if n>3:
        return endings[0]
    else:
        return endings[n]