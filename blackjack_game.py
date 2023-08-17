import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
             'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 1}

class Bank():
    
    def __init__(self, deposit):
        self.deposit = deposit
        
    def __str__(self):
        return f"Current balance is {self.deposit}$"
    
    def add(self, bet):
        self.deposit += bet
        print(f"Added {bet}$")
        
    def withdraw(self, bet):
        if self.deposit <= 0:
            print(f"Your balance is {self.deposit}$. You can't withdraw money :(")
        else:
            self.deposit -= bet
            print(f"{bet}$ was withdrawed")
            
class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    
    def __init__(self):
        
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)
    
    def shuffle(self):
        random.shuffle(self.all_cards)
        
    def deal_one(self):
        return self.all_cards.pop()
    
class Player:
    
    def __init__(self):
        self.all_cards = []
        self.value_of_cards = 0
        
    def add_cards(self, new_cards):
        if type(new_cards) == type([]):
            self.all_cards.extend(new_cards)
            print(f"{new_cards[0]} and {new_cards[1]}")
        else:
            self.all_cards.append(new_cards)
            print(f"{new_cards}")
    
    def sum_of_cards(self):
        self.value_of_cards = 0
        for card in self.all_cards:
            self.value_of_cards += card.value
        return self.value_of_cards
    
    def __str__(self):
        return f"Value of player's cards is {self.value_of_cards}"
    
class Dealer():
    
    def __init__(self):
        self.all_cards = []
        self.value_of_cards = 0
    
    def add_cards(self, new_cards):
        if type(new_cards) == type([]):
            self.all_cards.extend(new_cards)
            print(f"{new_cards[0]}")
        else:
            self.all_cards.append(new_cards)
            
    def sum_of_cards(self):
        self.value_of_cards = 0
        for card in self.all_cards:
            self.value_of_cards += card.value
        return self.value_of_cards
    
    def __str__(self):
        return f"Value of dealer's cards is {self.value_of_cards}"
    
deposit = int(input("How much do you want to deposit to the account? "))
account = Bank(deposit)

player = Player()
dealer = Dealer()
game_deck = Deck()

game_deck.shuffle()
game_on = True

bet = int(input("How much do you want to bet? "))
if account.deposit == 0:
    print(f"You don't have any money to withdraw :(")
    game_on = False
else:
    account.withdraw(bet)

while game_on:
        
    player.add_cards([game_deck.deal_one(), game_deck.deal_one()])
    dealer.add_cards([game_deck.deal_one(), game_deck.deal_one()])
    
    player_turn = True
    
    while player_turn:
        
        if player.all_cards[0].rank == "Ace" or player.all_cards[1].rank == "Ace":
            ace_value = True
            while ace_value:
                value = int(input("Do you want the ace value to be 1 or 11? "))
                if value == 1:
                    player.all_cards[-1].value = 1
                    ace_value = False
                elif value == 11:
                    player.all_cards[-1].value = 11
                    ace_value = False
                else:
                    print(f"{value} is a wrong value. Try again.")
            
        action = input("Hit or Stay? ")
        
        if action.lower() == 'hit':
            player.add_cards(game_deck.deal_one())
            
            if player.all_cards[-1].rank == "Ace":
                ace_value = True
                
                while ace_value:
                    value = int(input("Do you want the ace value to be 1 or 11? "))
                    if value == 1:
                        player.all_cards[-1].value = 1
                        ace_value = False
                    elif value == 11:
                        player.all_cards[-1].value = 11
                        ace_value = False
                    else:
                        print(f"{value} is a wrong value. Try again.")
            
            player_value = player.sum_of_cards()
            
            if int(player_value) > 21:
                print(f"Your score is {player_value}. You've lost the game :(")
                player_turn = False
                game_on = False
                break
            elif player_value == 21:
                print(f"Your score is {player_value}! You won!")
                account.add(bet * 2)
                player_turn = False
                game_on = False
                break
            
        elif action.lower() == "stay":
            player_turn = False
            
        else:
            print(f"{action} is wrong input. Try again.")
            
    if game_on == False:
        break
    
    dealer_turn = True
    
    while dealer_turn:
        
        dealer.add_cards(game_deck.deal_one())
        dealer_value = dealer.sum_of_cards()
        
        if dealer_value > 21:
            print(f"Your score is {dealer_value}. Player won.")
            account.add(bet * 2)
            dealer_turn = False
            game_on = False
            break
        elif dealer_value < 21 and dealer_value > player_value:
            print(f"Dealer has {dealer_value}. Dealer won the game.")
            dealer_turn = False
            game_on = False
            break
