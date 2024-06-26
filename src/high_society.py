import random
from datetime import datetime
from users import Player
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
from helper import show_image

"""
TO DO: 
11. Change card-display map (minor)
"""


    
class HighSocietyPlayer(Player):
    currency_denomination=[1000,2000,3000,4000,5000,8000,10000,12000,15000,20000,25000]

    def __init__(self,player:Player):
        super().__init__(player_id=player.player_id,name=player.player_name,dob=player.dob)
        self.cards=set()
        self.luxury_cards=set()
        self.available_money=set(self.currency_denomination)
        self.bid_money=set()
        self.active_bid=0
        self.luxury_score=0
        self.prestige_cards_count=0
        self.disgrace_cards_count={"minus-five":0,
                                   "half":0,
                                   "discard-one":0} 
        self.status=0
    
    
    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(player_id={self.player_id!r}, player_name={self.player_name!r}, dob={self.dob})"
    
    def __str__(self) -> str:
        return  f"{self.player_name}'s cards: {self.cards}, Status: {self.status}"

class CircularLinkedList:
    def __init__(self,player:HighSocietyPlayer, next=None) -> None:
        self.player=player
        self.next=next

class HighSocietyGame:
    MIN_PLAYERS=3
    MAX_PLAYERS=5
    card_display_map={
    "1":(1,"Eau De Parfum",'eau_de_parfum.jpeg'),
    "2":(2,"Champagne",'champagne.jpeg'),
    "3":(3,"Haute Cuisine",'haute_cuisine.jpeg'),
    "4":(4,"Casino",'casino.jpeg'),
    "5":(5,"Couture",'couture.jpeg'),
    "6":(6,'Vacances','vacances.jpeg'),
    "7":(7,"Objet D'art","objet_d'art.jpeg"),
    "8":(8,"Bijoux",'bijoux.jpeg'),
    "9":(9,"Dressage",'dressage.jpeg'),
    "10":(10,"Tourneé En Voilier",'tourneé_en_voilier.jpeg'),
    "2x-a":(11,"Avant Garde",'avant_garde.jpeg'),
    "2x-b":(12,"Joie de Vivre",'joie_de_vivre.jpeg'),
    "2x-c":(13,"Bon Vivant",'bon_vivant.jpeg'),
    "minus-five":(14,'Passé!','passé!.jpeg'),
    "half":(15,'Scandale!','scandale!.jpeg'),
    "discard-one":(16,"Faux Pas!",'faux_pas!.jpeg')
    }
    # card_display_map={
    #     'Eau De Parfum': (1, '1', 'eau_de_parfum.jpeg'), 
    #     'Champagne': (2, '2', 'champagne.jpeg'), 
    #     'Haute Cuisine': (3, '3', 'haute_cuisine.jpeg'), 
    #     'Casino': (4, '4', 'casino.jpeg'), 
    #     'Couture': (5, '5', 'couture.jpeg'), 
    #     'Vacances': (6, '6', 'vacances.jpeg'), 
    #     "Objet D'art": (7, '7', "objet_d'art.jpeg"), 
    #     'Bijoux': (8, '8', 'bijoux.jpeg'), 
    #     'Dressage': (9, '9', 'dressage.jpeg'), 
    #     'Tourneé En Voilier': (10, '10', 'tourneé_en_voilier.jpeg'), 
    #     'Avant Garde': (11, '2x', 'avant_garde.jpeg'), 
    #     'Joie de Vivre': (12, '2x', 'joie_de_vivre.jpeg'), 
    #     'Bon Vivant': (13, '2x', 'bon_vivant.jpeg'), 
    #     'Passé!': (14, 'minus-five', 'passé!.jpeg'), 
    #     'Scandale!': (15, 'half', 'scandale!.jpeg'), 
    #     'Faux Pas!': (16, 'discard-one', 'faux_pas!.jpeg')
    #     }

    CARD_TYPES=['luxury','prestige','disgrace']
    disgrace_cards=set(["minus-five","half","discard-one"])
    prestige_cards=set(["2x-a","2x-b","2x-c"])
    luxury_cards=set([*range(1,11)])
    # disgrace_cards=set(["Passé!","Scandale!","Faux Pas!"])
    # prestige_cards=set(["Avant Garde","Joie de Vivre","Bon Vivant"])
    # luxury_cards={'Eau De Parfum', 'Tourneé En Voilier', 'Vacances', 'Bijoux', \
    #               'Casino', 'Haute Cuisine', "Objet D'art", 'Dressage', 'Champagne', 'Couture'}
    colored_cards=prestige_cards
    colored_cards.add("half")
    IMGS_PATH='imgs'
    
    def __init__(self,game_id:int,game_name:str="HighSociety",players=[]):
        self.game_id=game_id
        self.game_name=game_name
        self.players=players
        self.num_of_players=0#len(self.players)
        self.count_colored_cards=0
        self.cards=set(self.card_display_map.keys())
        self.current_highest_bid=0
        self.round_table=CircularLinkedList(None)
        self.inactive_players=set()
        self.active_players=set()
        self.dummy=self.round_table

        self.create_game(self.players)


    def create_game(self,players):
        """
        
        """
        print("Welcome to High Society! ")

        self.num_of_players=int(input('Please enter the number of players for the game (3-5): '))
        if self.num_of_players<self.MIN_PLAYERS:
            raise Exception('Minimum of three players needed for the game!')
        if self.num_of_players>self.MAX_PLAYERS:
            raise Exception('Maximum of five players allowed for the game!')
        
        for i in range(self.num_of_players):
            player_name=input(f"\nPlayer {i+1}: \nPlease enter player name (alphanumeric): ")
            player_dob= input(f" Please enter their Date of Birth(optional) in dd/mm/yyyy format: ")
            if player_dob=="" or player_dob==" ":
                player_dob=None 
            player=Player(player_id=i+1, name=player_name, dob=player_dob)
            hs_player=HighSocietyPlayer(player)
            self.players.append(player)
            # hs_player=HighSocietyPlayer(players[i])
            # self.players_queue.append(hs_player.player_id)

            #Build circular Linked list
            node=CircularLinkedList(hs_player,None)
            self.round_table.next=node
            self.round_table=self.round_table.next
        self.round_table.next=self.dummy.next 
        self.round_table=self.round_table.next
        
        self.show_card(figure=1,img_path='high-society.jpeg',window_name='High Society')
        print("\nGame is ready to begin!\n")

    def update_hand_money(self,player:Player,money:int,card_type:str):
        """
        Function to update money of a player's hand based on his move (BID or PASS) and card type(Disgrace or other)
        Args:
            player: Player
            money: int
            card_type: str
        Returs:
            returns: None
        """
        if card_type==self.CARD_TYPES[2]:
            if money==0: #pass
                for money in player.bid_money:
                    player.available_money.add(money)

                player.active_bid=0
                player.bid_money=set()
            else:
                player.bid_money.add(money)
                player.active_bid+=money
                player.available_money.remove(money)
        else:
            if money==0: #pass
                for money in player.bid_money:
                    player.available_money.add(money)

                player.active_bid=0
                player.bid_money=set()
            else: #bid 
                player.bid_money.add(money)
                player.active_bid+=money
                player.available_money.remove(money)

    def update_hand_cards(self,player:Player, card:str, card_type:str):
        """
        Function to update a player's hand with a new card
        Args:
            player: Player
            card: str
            card_type: str
        Returns: 
            None
        """
        if card_type==self.CARD_TYPES[0]:
            player.luxury_score+=int(card)
            player.luxury_cards.add(card)
        elif card_type==self.CARD_TYPES[1]:
            player.prestige_cards_count+=1
        else:
            player.disgrace_cards_count[card]+=1

        player.cards.add(card)

        if player.disgrace_cards_count['discard-one']==1:
            if len(player.luxury_cards)>0:
                flag=False
                while not flag:
                    try:
                        discard_card=input(f"\nChoose a luxury card to discard from {player.luxury_cards}: ")
                        if discard_card not in player.luxury_cards:
                            raise Exception
                        else:
                            flag=True
                    except:
                        input("\nIncorrect Input! Try again.")

                player.cards.remove(discard_card)
                player.cards.remove('discard-one')
                player.luxury_cards.remove(discard_card)
                player.luxury_score-=int(discard_card)
                player.disgrace_cards_count['discard-one']-=1


    def move(self,player:Player,card_type:str):
        """
        This function takes user input for a move in the auction, 
        parses the input, and returns a boolean True if the user PASSED or False if he bid money.
        Args:
            player: Player
            card_type: str
        Returns: 
            None
        """
        move_flag=False
        if len(player.available_money)>0:
            input_message=f"\nWould you like to BID or PASS? \
                            \nEnter 0 to PASS or to make a bid, enter values(comma separated) from the following money denominations \n{sorted(list(player.available_money))}: "
        else:
            input_message=f"\nNo additional money left to BID. You have to PASS \
                            \nEnter 0 to PASS: "
        while not move_flag: #Run move until correct input is not entered by user
            try:
                player_move=str(input(input_message))                    
            except:
                print("Incorrect Input! Try again")
            if player_move=='0':
                self.update_hand_money(player,int(player_move),card_type)
                # move_flag=True
                return True
            else:
                bid_amount=0
                bid_money=player_move.split(',')
                for i in range(len(bid_money)):
                    assert int(bid_money[i]), "Non-numeric value passed as money! Enter a valid numeric value as money"
                    assert int(bid_money[i]) in player.available_money, f"Entered money {int(bid_money[i])} is not available in the denominations! Enter a valid denomination"
                    try:
                        money=int(bid_money[i])
                    except Exception as e:
                        print(f"Invalid input - Non-numeric value passed as money!")

                    try:
                        if money in player.available_money:
                            bid_amount+=money 
                        else:
                            raise Exception
                    except Exception as e:
                        print('Invalid input - Entered money is not available in the available denominations!\
                                            Enter a valid denomination')
                #check if active-bid is largest bid
                if player.active_bid+bid_amount<=self.current_highest_bid:
                    input_message=f"\nYour total bid of {player.active_bid+bid_amount} is not greater than the highest bid of {self.current_highest_bid}!\
                                    \nEither Enter 0 to PASS or increase your bid by entering from the following denominations {sorted(list(player.available_money))}: "
                else:
                    for money in bid_money:
                        self.update_hand_money(player, int(money), card_type)
                    self.current_highest_bid=player.active_bid
                    move_flag=True
        
        return False #False for a bid, return True for a PASS 
    
    def show_card(self,figure:int,img_path:str,window_name:str='High Society'):
        """
        Reads the image using open-CV
        """
        filepath=os.path.join(self.IMGS_PATH,img_path)
        img=cv2.imread(filepath)
        show_image(figure,window_name,img)

    def pick_a_card(self):
        """
        Randomly picks a card and returns the card and its card type
        Args: 
            None
        Returns:
            open_card: str
            card_type: str
        """
        key=str(input("\n\nPress a key and ENTER to reveal a card: "))
        open_card=random.choice(list(self.cards))
        self.cards.remove(open_card)
        card_type=self.find_card_type(open_card)
        return open_card,card_type

    def find_card_type(self,card):
        """
        Returns the card type from the following: disgrace, prestige, or luxury
        Args:
            card:str
        Returns:
            str
        """
        if card in self.disgrace_cards:
            return self.CARD_TYPES[2]
        elif card in self.prestige_cards:
            return self.CARD_TYPES[1]
        return self.CARD_TYPES[0]
    
    def check_end_of_game(self):
        """
        This function checks if end of game has reached and returns a Boolean.
        If number of colored cards equal 4, game is over, return True.
        """
        if self.count_colored_cards==4:
            return True
        return False
    
    def update_hand(self,player, card, card_type):
        self.update_hand_cards(player,card,card_type)
        self.compute_status(player)

    def show_game_status(self):
        """
        Shows the player's cards and its status during the game
        """
        print("\n CURRENT GAME STATUS:")
        print(f" Number of cards available for Auction: {len(self.cards)+1}")
        print(f" Number of cards auctioned: {16-len(self.cards)-1}")
        print(f" Number of colored cards auctioned: {max(0,self.count_colored_cards-1)}\n")

        info=[]
        i=0
        while i<self.num_of_players:
            player=self.round_table.player
            info.append([player.player_name,list(player.cards),player.status])
            self.round_table=self.round_table.next
            i+=1

        df=pd.DataFrame(data=info,columns=['Name','Cards','Current Status'])
        print(df)

    def show_winner(self):
        """
        Displays final status for each player and declares the winner. Handles a tie-breaking scenario.
        """
        node=self.dummy.next
        scores=[]
        i=0
        while i<self.num_of_players:
            player=self.round_table.player
            scores.append((player.status,player.player_name,sum(player.available_money)))
            self.round_table=self.round_table.next
            i+=1
        
        scores.sort(reverse=True)
        if scores[0][0]==scores[0][1]:
            if scores[0][2]==scores[1][2]:
                winning_message=f"It's a tie! Congratulations {scores[0][1]} and {scores[1][1]}, you are both winner!"
            else: 
                winning_message=f"\nCongratulations {scores[0][1]}! You are the winner!"
        else:
            winning_message=f"\nCongratulations {scores[0][1]}! You are the winner!"
            
        print("Final Scores:")
        for score, name,money_in_hand in scores:
            print(f"{name}: Score: {score}, Money left: {money_in_hand}")

        print(winning_message)

    
    def set_seed(self,seed:int=None):
        """
        Function to set the seed of random number generator
        """
        random.seed(a=seed)

        
    def run(self) -> None:
        """
        This function runs the auctioning process of High Society

        """
        end_game=False
        self.set_seed()
        while not end_game:
            open_card,card_type=self.pick_a_card()
            if open_card in self.colored_cards:
                self.count_colored_cards+=1
            self.show_card(figure=1,img_path=self.card_display_map[open_card][2],window_name='High Society')

            if not self.check_end_of_game():
                self.current_highest_bid=0
                self.inactive_players=set()
                self.active_players=set([player.player_name for player in self.players])
                
                self.show_game_status()
                print(f"\n\t\t\tNext up for Auction is {card_type} card: {open_card}")

                if card_type=='disgrace':    #disgrace card; Auction process: bid money to avoid card, pass to save money and instead collect card
                    pass_flag=False
                    while not pass_flag:
                        player=self.round_table.player
                        print(f"{player.player_name}'s turn to bid, your last bid: {player.active_bid}: ")
                        if not self.move(player, card_type): #check if player bid or passed
                            print("-------------------------------------------------")
                            print(f"Current Highest Bid: {self.current_highest_bid}")
                            self.round_table=self.round_table.next
                        else:
                            print(f"\nAuction Ended: {player.player_name} has Passed, and gets the card")
                            print("-----------------X-----------------X---------------")
                            self.update_hand(player,open_card,card_type)
                            pass_flag=True
                        
                else:   #luxury or presige cards; Auction process: bid money to win card, or pass to leave the auction 
                    while len(self.inactive_players)<self.num_of_players-1:
                        while self.round_table.player in self.inactive_players:
                            self.round_table=self.round_table.next
                        player=self.round_table.player
                        print("-------------------------------------------------")
                        print(f"Current Highest Bid: {self.current_highest_bid}")
                        print(f"Players still in auction: {self.active_players}")
                        print(f"{player.player_name}'s turn to bid, your last bid: {player.active_bid}; Denominations: {list(player.bid_money)}")
                        if self.move(player,card_type): #check if player bid or passed
                            print(f"{player.player_name} has Passed")
                            self.inactive_players.add(player)
                            self.active_players.remove(player.player_name)

                        self.round_table=self.round_table.next
                    #Auction over-Assign card to auction winner
                    
                    while self.round_table.player in self.inactive_players:
                        self.round_table=self.round_table.next
                    winner=self.round_table.player
                    winner.active_bid=0
                    print(f"\nAuction Ended: {winner.player_name} gets the card")
                    print("-----------------X-----------------X---------------")
                    self.update_hand(winner, open_card, card_type)
                
                #End of auction: resolve money for each player 
                i=0
                while i<self.num_of_players:
                    self.round_table.player.active_bid=0
                    # if card_type==self.CARD_TYPES[2]:
                    self.round_table.player.bid_money=set()
                    self.compute_status(self.round_table.player)
                    self.round_table=self.round_table.next
                    i+=1
                
                # self.round_table=self.round_table.next
            else:
                end_game=True

        # score and declare winner
        self.show_game_status()
        print("\n\nEnd of Game - Fourth colored card revealed\n")
        cv2.destroyAllWindows()
        self.show_winner()


    def compute_status(self, player):
        """
        Function computes the running status of the player
        """
        minus_five=0
        half=1
        if player.disgrace_cards_count['minus-five']==1:
            minus_five=-5
        if player.disgrace_cards_count['half']==1:
            half=0.5
        
        player.status=(player.luxury_score+minus_five)*half
        if player.prestige_cards_count:
            player.status*=(2*player.prestige_cards_count)


    def get_player_order(self):
        pass

    def __str__(self) -> str:
        return f"ID={self.game_id}, \nGame Name={self.game_name}, \nNumber of Players={self.num_of_players}"
    
    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(game_id={self.game_id!r}, game_name={self.game_name!r}, num_of_players={self.num_of_players!r})"



def add_players(num_players):
    return None


#initialize players
player_info=[
            ('Eshaan','16/02/1990'),
            ('Vivan','31/01/1991'),
            ('Radhika','11/03/1992'),
            ('Sahil','15/07/1991'),
            ('Sneha','21/12/1988'),
            ('Rama','20/03/1961')
            ]
players=[]
for i in range(len(player_info)):
    player=Player(player_id=i+1,name=player_info[i][0],dob=player_info[i][1])
    players.append(player)

#initialize game
game1=HighSocietyGame(27,game_name='Trial',players=[])
game1.run()