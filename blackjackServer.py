# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 19:18:17 2021

@author: Ghasif, Yehua, Tong
"""

# Imports
import socket
import random
from _thread import *

# Server setup
ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 1233
ThreadCount = 0
ServerSocket.bind(('', port))

# Wait for a Connection
print('Waitiing for a Connection..')
ServerSocket.listen(10)

# Thread function
def threaded_client(connection, num):
    
    # Declare the suits/ranks of cards along with the values associated with them
    suits = ["♣♣♣", "♦♦♦", "♥♥♥", "♠♠♠"]
    ranks = ["2", "3", "4", "5", "6",
                   "7", "8", "9", "10", "Jack", "Queen", "King","Ace"]
    values = {"2":2,"3":3,"4":4, "5":5, "6":6,
                   "7":7, "8":8, "9":9, "10":10, "Jack":10, "Queen":10, "King":10,"Ace":1}
    
    # Array that represents the Dealer's Hand
    dealer_Hand = []
    
    # Array that represents the Player's Hand
    player_Hand = []
    
    # Boolean to represent if the game is currently being played or not
    playing = True
    
    # Function that adds a card to the player/dealer hand (array) passed in
    def add_Cards(hand):
        card = (ranks[random.randint(0,12)],suits[random.randint(0,3)])
        hand.append(card)
    
    # Function that sums up the player/dealer hand (array) passed in and returns the total value
    def get_Value(hand):
        total = 0
        aces = 0
        for x in hand: 
            val = values[x[0]]
            total += val
            if (x[0]=="Ace"):
                aces+=1
        while total <= 11 and aces:
            total += 10
            aces -= 1
        return total
    
    # Function that formats a specific card from the player/dealer hand (array) and index (int) passed in and returns string representation of that card
    def show_Card(hand,index):
        ret = hand[index][0]+" of "+hand[index][1]
        return ret
    
    # Function that formats the player/dealer hand (array) passed in and returns string value of ASCII art cards
    def print_Deck(hand):
        if (hand == player_Hand):
            ret = "Player Hand: \n"
        if (hand == dealer_Hand):
            ret = "Dealer Hand: \n"
        card = ""
        maxLen = len(hand)
        for x in range (maxLen):
            rank = str(hand[x][0])
            suit = str(hand[x][1])
            card = "=========\n|"+rank[0]+"      |\n|   "+suit[0]+"   |\n|      "+rank[0]+"|\n========="
            ret += card+"\n"
        return ret
    
    # Function that resets the player & dealer hand and adds 2 cards to each hand
    def starting_Hand ():
        player_Hand.clear()
        dealer_Hand.clear()
        add_Cards(dealer_Hand)
        add_Cards(dealer_Hand)
        add_Cards(player_Hand)
        add_Cards(player_Hand)
    
    # Function that formats the initial hand represetnations and returns string value of it
    def init_cards():
        init_cards = "DEALER: "+show_Card(dealer_Hand,0)+"; " +"(HIDDEN CARD) \nPLAYER: "+show_Card(player_Hand,0)+"; "+show_Card(player_Hand,1)
        return init_cards
    
    # Function that is called upon when player chooses to hit, adding a card to the player hand and playing out the dealers turn
    def hit():
        add_Cards(player_Hand)   
        while get_Value(dealer_Hand) < 17:
            add_Cards(dealer_Hand)   
    
    # Function that is called upon when player chooses to stand, playing out the delaers turn
    def stand():
        while get_Value(dealer_Hand) < 17:
            add_Cards(dealer_Hand)   
    
    # Function that formats the current game being played and returns string value of it
    def oldGame():
        currentReply = "DEALER: "+show_Card(dealer_Hand,0)+"; " +show_Card(dealer_Hand,1)+" \nPLAYER: "+show_Card(player_Hand,0)+"; "+show_Card(player_Hand,1)+"\nDealer Hand Value is: "+str(get_Value(dealer_Hand))+"\nPlayer Hand Value is: "+str(get_Value(player_Hand))+"\n"
        playerDeck = print_Deck(player_Hand)
        dealerDeck = print_Deck(dealer_Hand)
        return currentReply+"\n"+dealerDeck+"\n"+playerDeck+"\n"
    
    # Function that formats the new game and returns the string value of it
    def newGame():
        return init_cards()+"\nDealer Hand Value is: "+str(values[dealer_Hand[0][0]])+"\nPlayer Hand Value is: "+str(get_Value(player_Hand))+hit_msg
    
    # Function that is called upon when player chooses to stand, checks the game status and returns the status of the game to be evaluated
    def checkStatusStand():
        ret = ""
        if get_Value(player_Hand)==21:
            ret = "YOU WIN. You got a Blackjack!\n"+'Press "ENTER" to start a new game!'
        elif get_Value(dealer_Hand)==21:
            ret = "YOU LOSE. Dealer got a Blackjack\n"+'Press "ENTER" to start a new game!'
        elif get_Value(player_Hand)>21:
            ret = 'YOU LOSE. You busted\n'+'Press "ENTER" to start a new game!'
        elif get_Value(dealer_Hand)>21: 
            ret = "YOU WIN. Dealer busted\n"+'Press "ENTER" to start a new game!'
        elif get_Value(player_Hand)<get_Value(dealer_Hand):
            ret = 'YOU LOSE. Dealer has a higher score than You\n'+'Press "ENTER" to start a new game!'
        elif get_Value(player_Hand)>get_Value(dealer_Hand):
            ret = "YOU WIN. Your score is higher than the Dealer\n"+'Press "ENTER" to start a new game!'
        elif get_Value(player_Hand)==get_Value(dealer_Hand):
            ret = "ITS A TIE. Push!\n"+'Press "ENTER" to start a new game!'
        return ret
    
    # Function that is called upon when player chooses to hit, checks the game status and returns the status of the game to be evaluated
    def checkStatusHit():
        ret = ""
        if get_Value(player_Hand)==21:
            ret = "YOU WIN. You got a Blackjack!\n"+'Press "ENTER" to start a new game!'
        elif get_Value(dealer_Hand)==21:
            ret = "YOU LOSE. Dealer got a Blackjack\n"+'Press "ENTER" to start a new game!'
        elif get_Value(player_Hand)>21:
            ret = 'YOU LOSE. You busted\n'+'Press "ENTER" to start a new game!'
        elif get_Value(dealer_Hand)>21: 
            ret = "YOU WIN. Dealer busted\n"+'Press "ENTER" to start a new game!'
        elif get_Value(dealer_Hand)>get_Value(player_Hand) and get_Value(player_Hand)<21:
            ret = ""
        elif get_Value(player_Hand)<get_Value(dealer_Hand):
            ret = 'YOU LOSE. Dealer has a higher score than You\n'+'Press "ENTER" to start a new game!'
        elif get_Value(player_Hand)>get_Value(dealer_Hand):
            ret = "YOU WIN. Your score is higher than the Dealer\n"+'Press "ENTER" to start a new game!'
        return ret
    
    # Starts the very first game and sends a message the player
    hit_msg = "\nDo you want to hit or stand?"
    starting_Hand()
    connection.send(str.encode(init_cards()+"\nDealer Hand Value is: "+str(dealer_Hand[0][0])+"\nPlayer Hand Value is: "+str(get_Value(player_Hand))+hit_msg))

    # While loop used to play the game, fucntions while the game is being played, playing (boolean) = True 
    while (playing==True):
        # Receives the input from the player on whether they want to hit or stand
        data = connection.recv(1024).decode('utf-8')
        # If statement that checks to see if the player choose to hit
        if (data == "hit"):
            hit()
            # If statement that checks if the game has ended; sets playing (boolean) to False
            if (checkStatusHit()!=""):
                playing=False
            # Sends message of the current game
            connection.send(str.encode(oldGame()+"\n"+checkStatusHit()))
        # If statement that checks to see if the player choose to stand
        elif (data == "stand"):
            stand()
            # If statement that checks if the game has ended; sets playing (boolean) to False
            if (checkStatusStand()!=""):
                playing=False
            # Sends message of the current game
            connection.send(str.encode(oldGame()+"\n"+checkStatusStand()))
        # If statement that checks if the game has ended, playing (boolean) = False; resets the game, and sets playing (boolean) to True
        if(playing==False): 
            starting_Hand()
            connection.send(str.encode("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n                                 NEW GAME\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"+newGame()))
            playing=True                                                                                           
    connection.close()

# Main while loop
while True:
    Client, address = ServerSocket.accept() #accept new client
    print('Connected to: ' + address[0] + ':' + str(address[1])) #print client address
    start_new_thread(threaded_client, (Client, ThreadCount, )) #create new thread with client connection and id
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()