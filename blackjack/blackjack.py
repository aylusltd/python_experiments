import random
import constants
import deck

deck = deck.Deck()
bank = constants.starting_bank
# bank = 100

def show_all_hands(hands):
    for hand in hands:
        displayHand(hand)

def resolve(hands, dealerHand, bets, display=True):
    winnings=0
    print "Dealer has the following cards in their hand"      
    dealerScore = displayHand(dealerHand, True)

    if dealerScore > 21:
        print "Dealer Busted!"
    current_hand=1
    for hand in hands:
        print "Hand " + str(current_hand) +":"
        userScore = displayHand(hand, display)
        if userScore == 21 and dealerScore != 21:
            print "Black Jack on your " + str(current_hand) + constants.get_ending(current_hand) + " hand."
            winnings+=bets[current_hand-1]*constants.black_jack_multiplier
        elif (dealerScore > 21 or dealerScore < userScore) and userScore < 22:
            print "You win your " + str(current_hand) + constants.get_ending(current_hand) + " hand."
            winnings += bets[current_hand-1]
        elif dealerScore == userScore:
            print "Push on your " + str(current_hand) + constants.get_ending(current_hand) + " hand."
        else:
            winnings -= bets[current_hand-1]
            print "You lose your " + str(current_hand) + constants.get_ending(current_hand) + " hand."
        current_hand+=1
    return winnings


def get_bet():
    print "You have $"+str(bank)+"."
    bet=0
    while bet<constants.min_bet or bet > bank:
        print "How much would you like to bet?"
        bet=raw_input("Minimum bet: $1\n")
        try:
            bet=int(bet)
        except:
            print "Invalid bet"
    return bet

def displayHand(hand, display=True):
    AceCount=0
    handScore=0
    handString=""
    for card in hand:
        handString+= card["display"] + card["suit"] + " "
        handScore+=card["value"]
        if card["value"]==1:
            AceCount+=1
        while AceCount > 0:
            if handScore < 11:
                handScore+=10
            AceCount-=1
    if display:
        print handString
        print handScore
    return handScore

newGame = "y"
count=0
resolved=False
#main loop
while newGame == "y":
    bets=[get_bet()]
    can_split=[]
    hand_number=0
    hands=[]
    gameOver = False
    dealerDone = False
    hands.append([deck.deal()])
    dealerHand=[deck.deal()]
    hands[hand_number].append(deck.deal())
    dealerHand.append(deck.deal())

    
    if hand_number > 0:
        print "You have the following hands:"
        show_all_hands(hand)
        print "Playing hand " + str(hand_number+1)

    print "You have the following cards in your hand"
    handScore=displayHand(hands[hand_number])
    if handScore == 21:
            print "BlackJack"
            bank+=resolve(hands, dealerHand, bets, display=False)
            resolved = True
            gameOver = True
    while not gameOver:
        can_split.append(True)
        if can_split[hand_number]:
            action = raw_input("(D)ouble Down, (H)it, (S)plit, or S(t)and\n")
        else:
            action = raw_input("(H)it, or S(t)and\n")
        if action == "H" or action == "h":
            hands[hand_number].append(deck.deal())
            handScore=displayHand(hands[hand_number])
            can_split[hand_number]=False
            if handScore > 21:
                print "Busted!"
                gameOver = True
        elif (action == "D" or action == "d") and can_split[hand_number]:
            hands[hand_number].append(deck.deal())
            handScore=displayHand(hands[hand_number], False)
            bets[hand_number]*=2
            if handScore > 21:
                print "Busted!"
            gameOver = True
        elif (action == "S" or action == "s") and can_split[hand_number] and hands[hand_number][0]["name"]==hands[hand_number][1]["name"]:
            # Split
            # print "not yet supported"
            hands.append([hands[hand_number][1]])
            hands[hand_number][1]=deck.deal()
            hands[len(hands)-1].append(deck.deal())
            gameOver = True
        else:
            gameOver = True
    while not dealerDone:
        dealerScore=displayHand(dealerHand,False)
        if dealerScore < 17:
            dealerHand.append(deck[count])
            count+=1
        else:
            dealerDone=True

    if not resolved:
        bank+=resolve(hands, dealerHand, bets)

    newGame=raw_input("Press 'y' to play again\n")
    if newGame == "y":
        if deck.current_card > 20:
            deck.shuffle()
    else:
        print "You ended with $" + str(bank)
