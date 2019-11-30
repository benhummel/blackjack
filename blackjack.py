import random
import time

all_cards = [
	"2S","3S","4S","5S","6S","7S","8S","9S",
	"10S","JS","QS","KS","AS","2H","3H","4H",
	"5H","6H","7H","8H","9H","10H","JH","QH",
	"KH","AH","2C","3C","4C","5C","6C","7C",
	"8C","9C","10C","JC","QC","KC","AC","2D",
	"3D","4D","5D","6D","7D","8D","9D","10D",
	"JD","QD","KD","AD",
]

face_cards = ["J", "Q", "K", "A"]

############ game functions
def deal_card(): 
	# returns a random card from the deck, then removes that card from the deck
	# shuffles if deck runs out of cards
	global deck
	if len(deck) < 1: # when the deck runs out, reshuffle
		deck = all_cards
		print("Shuffling deck")
	card_index = random.randrange(0,len(deck))
	this_card = deck[card_index]
	deck.remove(this_card)
	return this_card

def get_player_bet():
	print("Your bank: ---> $" + str(balance))
	time.sleep(0.75)  # sleep
	print("How much do you want to bet?")
	time.sleep(0.75)  # sleep
	this_bet = int(raw_input())
	if this_bet > balance:
		print("You don't have that much. Your balance is " + str(balance))
		return(get_player_bet())
	print("You bet $" + str(this_bet))
	time.sleep(0.75)  # sleep
	print("You have $" + str(balance - this_bet) + " left")
	return this_bet


def offer_player_options():
	print("Hit (h), Double Down (d), Stand (s)")
	# print("Double down (d)")
	# if player_cards[0] == player_cards[1]:
	# 	print("Split (p)")
	play = raw_input()
	return play

def print_player_cards(cards):
	print("Your cards: " + str(cards))

def print_dealer_cards(cards):
	print("Dealer's cards: " + str(cards)) 

def end_round(outcome, bet):
	global balance
	if outcome == "lose":
		print("You lose!")
		balance = balance - bet
	elif outcome == "win":
		print("*** You win! ***")
		time.sleep(0.75)  # sleep
		print("You won $" + str(bet) + "!")
		time.sleep(0.75)  # sleep
		balance = balance + bet
		time.sleep(0.75)  # sleep
		print("Starting a new round...")
		time.sleep(1.5)  # sleep
	elif outcome == "push":
		print("Push!")
	else:
		print("Error")
		return 1

def get_card_value(card):
	# returns int for value of card
	this_card_value = 0
	card = card[:len(card)-1] 
	if card in face_cards[0:3]: #J Q K
		this_card_value = 10
	elif card == "A":
		this_card_value = 11
	else:
		this_card_value = card
	return this_card_value

def calculate_hand_value(hand):
	current_hand_value = 0
	num_aces = 0

	for card in hand:
		this_card_value = int(get_card_value(card))
		current_hand_value += this_card_value
		if this_card_value == 11:
			num_aces = num_aces + 1

	for i in range(num_aces):  
		if current_hand_value > 21:
			current_hand_value -= 10

	return current_hand_value

def check_for_blackjack(hand): 
	if calculate_hand_value(hand) == 21:
		return True
	else:
		return False


def player_turn(hand):
	global bet
	# offer player options
	print("You have " + str(calculate_hand_value(hand)) + " against the dealer's " + str(get_card_value(dealer_cards[0]))) 

	time.sleep(0.75)  # sleep

	if calculate_hand_value(hand) > 21:
		print("You busted!")
		time.sleep(0.75)  # sleep
		return calculate_hand_value(hand)

	play = offer_player_options()

	if play == "s":
		print("You stand at " + str(calculate_hand_value(hand)))
		time.sleep(0.75)  # sleep
		return calculate_hand_value(hand)
	elif play == "h":
		hand.insert(len(hand), deal_card())
		print_player_cards(hand)
		time.sleep(0.75)  # sleep
		return(player_turn(hand))
	elif play == "d":
		bet = bet * 2
		print("Doubling down!")
		time.sleep(0.75)  # sleep
		hand.insert(len(hand), deal_card())
		time.sleep(0.75)  # sleep
		print_player_cards(hand)
		print("You have " + str(calculate_hand_value(hand)) + " against the dealer's " + str(get_card_value(dealer_cards[0]))) 
		time.sleep(0.75)  # sleep
		return calculate_hand_value(hand)
	else:
		print("Invalid selection, try again.")
		time.sleep(0.75)  # sleep
		return(player_turn(hand))

def dealer_turn(dealer_cards):
	print("Dealer has " + str(calculate_hand_value(dealer_cards)))
	time.sleep(0.75)  # sleep
	print_dealer_cards(dealer_cards)
	time.sleep(0.75)  # sleep
	while calculate_hand_value(dealer_cards) < 17:
		print("Dealer hits")
		dealer_cards.insert(len(dealer_cards), deal_card())
		time.sleep(0.75)  # sleep
		print_dealer_cards(dealer_cards)
		time.sleep(0.75)  # sleep
		print("Dealer has " + str(calculate_hand_value(dealer_cards)))
		time.sleep(0.75)  # sleep
		if calculate_hand_value(dealer_cards) > 21:
			print("Dealer busted!")
			time.sleep(0.75)  # sleep
			return calculate_hand_value(dealer_cards)
		time.sleep(0.75)  # sleep
	print("Dealer stands at " + str(calculate_hand_value(dealer_cards)))
	time.sleep(0.75)  # sleep
	return calculate_hand_value(dealer_cards)



print("Welcome to Blackjack!") # only happens once
time.sleep(0.75)  # sleep
deck = all_cards
balance = 100

while balance > 0:  # game takes place inside this loop; play until out of $

	bet = get_player_bet()
	time.sleep(0.75)  # sleep

	# initialize empty hands each round
	player_cards = list()
	dealer_cards = list()

	# deal 2 cards per player
	player_cards.insert(len(player_cards), deal_card())
	dealer_cards.insert(len(dealer_cards), deal_card())
	player_cards.insert(len(player_cards), deal_card())
	dealer_cards.insert(len(dealer_cards), deal_card())

	print("**************")
	print_player_cards(player_cards)
	print("Dealer's cards: " + str(dealer_cards[0])) # keep dealer's second card hidden
	print("**************")

	time.sleep(1.25)  # sleep

	# if dealer has blackjack, player loses
	if check_for_blackjack(dealer_cards):
		# TODO: offer insurance
		print("Dealer has blackjack!")
		print_player_cards(player_cards)
		print_dealer_cards(dealer_cards)
		end_round("lose", bet)

	# is player has blackjack, player wins
	elif check_for_blackjack(player_cards):
		print("You got blackjack!")
		print_player_cards(player_cards)
		print_dealer_cards(dealer_cards)
		bet = bet * 1.5 # 3:2 payout
		end_round("win", bet)

	# assuming no blackjacks, now the player goes
	else:
		player_outcome = player_turn(player_cards) # returns the value of player's hand, or 0 for bust
		if player_outcome > 21:
			print("You busted!")
			end_round("lose", bet)
		else:
			dealer_outcome = dealer_turn(dealer_cards)
			if dealer_outcome > 21:
				end_round("win", bet)
			else:
				if dealer_outcome > player_outcome:
					end_round("lose", bet)
				elif dealer_outcome == player_outcome:
					end_round("push", bet)
				elif dealer_outcome < player_outcome:
					end_round("win", bet)
				else:
					print("Error - scores don't make sense!")

print("You're out of money!")
time.sleep(0.75)  # sleep
print("Just like Vegas...")
time.sleep(0.75)  # sleep
print("Time to go home to your shitty hotel room!")
time.sleep(0.75)  # sleep
print("GAME OVER")
