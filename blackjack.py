
import random
import time

class Card():
    ranks = [None, 'Ace', '2','3','4','5','6','7','8','9','10',
                'Jack','Queen','King']
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    values = {'Ace':11, '2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,
                'Jack':10,'Queen':10,'King':10}

    
    def __init__(self, r, s):
        self.rank = r
        self.suit = s

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck():

    def __init__(self):
        self.deck = []
        for r in Card.ranks[1:]:
            for s in Card.suits:
                self.deck.append(Card(r, s))
        random.shuffle(self.deck)


    def draw(self, index = 0):
        drawnCard = self.deck[index]
        del self.deck[index]
        return drawnCard

class Dealer():
    def __init__(self):

        # Represents cards in hand
        self.hand = []

        # Point value of cards in hand
        self.score = 0

        #Number of aces in hand that can be changed from 11 to 1
        self.aceFlips = 0 

        self.validTurn = True

        # False if score <= 21
        self.isBusted = False
        
    
    def __str__(self):
        cardsInHand = []
        for card in self.hand:
            cardsInHand.append(str(card))
        return str(cardsInHand)

    def scoreAdd(self, card):
        self.score += Card.values[card.rank]

    def bustedCheck(self):
        if self.score > 21:
            if self.aceFlips > 0:
                self.aceFlip()
            else: 
                self.isBusted = True
        elif self.score == 21:
            if isinstance(self, Player):
                print("Blackjack!!!")
            else:
                print("Dealer has Blackjack :'(")
            self.validTurn = False

    def limitCheck(self):
        if 21 > self.score >= 17:
            self.validTurn = False

            print("Dealer stands.")

    def aceFlip(self):
        time.sleep(1.0)
        print("An ace in the Dealer's hand has changed from 11 to 1.")
        self.score -= 10
        self.aceFlips -= 1
        time.sleep(0.5)
        print(f"Their new score is {self.score}")
    

class Player(Dealer):
    
    def __init__(self):
        super().__init__()

    def aceFlip(self):
        if self.aceFlips > 1:
            time.sleep(1.0)
            print("An ace in your hand has changed from 11 to 1.")
            self.score -= 10
            self.aceFlips -= 1
            time.sleep(0.5)
            print(f"Your new score is {self.score}.")


class Blackjack():

    def __init__(self):
        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck()

        self.playerDraw()
        self.dealerDraw()
        self.playerDraw()
        self.player.bustedCheck()

    def playGame(self):
        self.playerTurn()
        if self.player.isBusted == True:
            self.results()
        else:
            self.dealerTurn()
            self.results()
        

    def playerTurn(self):
        while self.player.validTurn and not self.player.isBusted:
            time.sleep(0.5)
            action = promptClient("\nWould you like to hit or stand?\nEnter 'h' to hit, 's' to stand, or 'v' to view hand: ", ['h', 's', 'v'])
            if action == 'v':
                print("\nYour hand: " + str(self.player))
                print("Score: [You: " + str(self.player.score) + ", Dealer: " + str(self.dealer.score) + "]\n")
                time.sleep(1.0)
            elif action == 'h':
                print("\nDrawing card...")
                self.playerDraw()
                time.sleep(0.5)
                self.player.bustedCheck()
            else:
                print("\nYou choose to stand. Dealer's turn!")
                self.player.validTurn = False

    def playerDraw(self):
        time.sleep(1.5)
        newCard = self.deck.draw()
        if newCard.rank == 'Ace':
            self.player.aceFlips += 1
        self.player.hand.append(newCard)
        self.player.scoreAdd(newCard)
        print("\nYou draw the " + str(newCard) + ".")
        time.sleep(0.5)
        print(f"\nScore: [You: {self.player.score}, Dealer: {self.dealer.score}]")

    def dealerTurn(self):
        while self.dealer.validTurn and not self.dealer.isBusted:
            self.dealerDraw()
            time.sleep(0.5)
            self.dealer.bustedCheck()
            self.dealer.limitCheck()
            
    def dealerDraw(self):
        time.sleep(1.0)
        newCard = self.deck.draw()
        if newCard.rank == 'Ace':
            self.dealer.aceFlips += 1
        self.dealer.hand.append(newCard)
        self.dealer.scoreAdd(newCard)
        print("\nThe dealer draws the " + str(newCard))
        time.sleep(0.5)
        print(f"\nScore: [You: {self.player.score}, Dealer: {self.dealer.score}]")

    def results(self):
        time.sleep(0.75)
        if self.player.isBusted:
            print("\nOh no! You busted!")
            print(f"\nDealer wins. The final score is:\nDealer: {self.dealer.score}, You: {self.player.score}")
        elif self.dealer.isBusted:
            print("\nDealer busted!")
            print(f"\nYou win! The final score is:\nDealer: {self.dealer.score}, You: {self.player.score}")
        elif self.player.score > self.dealer.score:
            print(f"\nYou win! The final score is:\nDealer: {self.dealer.score}, You: {self.player.score}")
        elif self.dealer.score > self.player.score:
            print(f"\nDealer wins. The final score is:\nDealer: {self.dealer.score}, You: {self.player.score}")
        else:
            print(f"\nDraw. Everybody wins? The final score is:\nDealer: {self.dealer.score}, You: {self.player.score}")
    

def promptClient(prompt, responses):
    userReply = input(prompt)
    while userReply not in responses:
        print("Invalid Response. Please Try Again.")
        userReply = input(prompt)
    return userReply


if __name__ == '__main__':
    replay = True
    print("\nWelcome to Blackjack! Now dealing cards...")
    while replay:
        game = Blackjack()
        game.playGame()
        status = promptClient("\nWould you like to play again?\nEnter 'y' for yes, 'n' for no: ",['y', 'n'])
        if status == 'n':
            replay = False
            print("\nHope you enjoyed! Goodbye!\n")
        else:
            print("Restarting game...")