import random
import datetime

class Card( object ):
    """ Model a playing card. """

    # Rank is an int (1-13), where aces are 1 and kings are 13.
    # Suit is an int (1-4), where clubs are 1 and spades are 4.
    # Value is an int (1-10), where aces are 1 and face cards are 10.

    # List to map int rank to printable character (index 0 used for no rank)
    rank_list = [' x',' A',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10',' J',' Q',' K']

    # List to map int suit to printable character (index 0 used for no suit)
    #suit_list = ['x','\u2663','\u2666','\u2665','\u2660']
    suit_list = ['x','h','d','c','s']
    
    def __init__( self, rank=0, suit=0 ):
        """ Initialize card to specified rank (1-13) and suit (1-4). """
        self.__rank = 0
        self.__suit = 0
        self.__face_up = None
        # Verify that rank and suit are ints and that they are within
        # range (1-13 and 1-4), then update instance variables if valid.
        if type(rank) == int and type(suit) == int:
            if rank in range(1,14) and suit in range(1,5):
                self.__rank = rank
                self.__suit = suit
                self.__face_up = True
        
    def rank( self ):
        """ Return card's rank (1-13). """
        return self.__rank

    def value( self ):
        """ Return card's value (1 for aces, 2-9, 10 for face cards). """
        # Use ternary expression to determine value.
        return self.__rank if self.__rank < 10 else 10

    def suit( self ):
        """ Return card's suit (1-4). """
        return self.__suit
    
    def is_face_up( self ):
        """ Returns True if card is facing up."""
        return self.__face_up
    
    def flip_card( self ):
        """ Flips card between face-up and face-down"""
        self.__face_up = not self.__face_up

    def __str__( self ):
        """ Convert card into a string (usually for printing). """
        # Use rank to index into rank_list; use suit to index into suit_list.
        if self.__face_up:
            return "{}{}".format( (self.rank_list)[self.__rank], \
                                  (self.suit_list)[self.__suit] )
        else:
            return "{}{}".format( " X", "X")
        # version to print Card calls for developing tests
        #return "cards.Card({},{})".format( self.__rank, self.__suit )

    def __repr__( self ):
        """ Convert card into a string for use in the shell. """
        return self.__str__()
        
    def __eq__( self, other ):
        """ Return True, if Cards of equal rank and suit; False, otherwise. """
        if not isinstance(other, Card):
            return False
            
        return self.rank() == other.rank() and self.suit() == other.suit()
        
class Deck( object ):
    """ Model a deck of 52 playing cards. """

    # Implement the deck as a list of cards.  The last card in the list is
    # defined to be at the top of the deck.

    def __init__( self ):
        """ Initialize deck--Ace of clubs on bottom, King of spades on top. """
        self.__deck = [Card(r,s) for s in range(1,5) for r in range(1,14)]

    def shuffle( self ):
        """ Shuffle deck using shuffle method in random module. """
        random.shuffle(self.__deck)

    def deal( self ):
        """ Return top card from deck (return None if deck empty). """
        # Use ternary expression to guard against empty deck.
        return self.__deck.pop() if len(self.__deck) else None

    def is_empty( self ):
        """ Return True if deck is empty; False, otherwise """
        return len(self.__deck) == 0

    def __len__( self ):
        """ Return number of cards remaining in deck. """
        return len(self.__deck)
    
    def __str__( self ):
        """ Return string representing deck (usually for printing). """
        return ", ".join([str(card) for card in self.__deck])
            
    def __repr__( self ):
        """ Return string representing deck (for use in shell). """
        return self.__str__()

    def display( self, cols=13 ):
        """ Column-oriented display of deck. """
        for index, card in enumerate(self.__deck):
            if index%cols == 0:
                print()
            print("{:3s} ".format(str(card)), end="" )
        print()
        print()
        
        
class RandomPlayer ( object ):
    ''' Plays or makes moves on game randomly '''
    
    
    def __init__( self ):
        pass
    
    
    
    ''' FINDING ALL THE POSSIBLE MOVES AS A DICT OF LISTS '''
    def find_moves(board_list,tableau_dict):
        moves_dict, moves = {}, 1
        for i in range(7):
            temp = board_list[:]
            if len(temp[i]) != 0:
                sc = temp[i][len(temp[i])-1]
                rsc = sc.rank()
                if rsc == 1:
                    count = 0
                    for k in range(len(temp[i])-1):
                        if temp[i][k].is_face_up() and temp[i][k+1].suit()==sc.suit():
                            if temp[i][k].rank()-temp[i][k+1].rank()==1:
                                count += 1
                    if count == 12:
                        moves_dict[moves] = ['Foundation',i+1,len(temp[i])-13]
                        moves += 1
                for tableau in temp:
                    if sc not in tableau:
                        for card in tableau:
                            if card.is_face_up():
                                if rsc - card.rank() == 1 and card.suit()==sc.suit():
                                    moves_dict[moves] = [i+1,temp.index(tableau)+1,tableau.index(card)+1]
                                    moves += 1
            else:
                for tableau in temp:
                    for card in tableau:
                        if card.is_face_up():
                            if card.rank() == 13:
                                if tableau.index(card) != 0:
                                    moves_dict[moves] = [i+1,temp.index(tableau)+1,tableau.index(card)+1]
                                    moves += 1
       
        ##CHOOSE ONE OF THE MOVES RANDOMLY
        if moves != 1:
            rand_number = random.randint(1,moves-1)
            return moves_dict[rand_number]
        elif moves == 1 and len(tableau_dict['Stock']) != 0:
                return 'Deal'
        else:
            moves = None
            return moves
    
    
    ''' REARRANGE THE BOARD USING ONE MOVE(LIST) IN moves_dict
            CAN BE A METHOD IN GAME CLASS USING try:except '''
    def make_move(move,board_list,tableau_dict,total_moves,score,Killgame):
        
        if move != None:
            total_moves += 1
            if move != 'Deal' and move[0] != 'Foundation':
                i, i1, i2 = move
                temp_list = board_list[i1-1][i2-1:]
                board_list[i1-1] = board_list[i1-1][:i2-1]
                board_list[i-1].extend(temp_list)
                
                    
            elif move[0] == 'Foundation':
                i,start = move[1:]
                temp_list = board_list[i-1][start:]
                board_list[i-1] = board_list[i-1][:start]
                tableau_dict['Foundation'].append(temp_list)
                score += 1300
            
            
            elif move == 'Deal':
                for card in tableau_dict['Stock']:
                    card.flip_card()
                for i in range(3):
                    card = tableau_dict['Stock'].pop(2-i)
                    board_list[i].append(card)
                
      
        else:
            Killgame = True
            
        return score,total_moves,Killgame

    
class Game ( object ):
    ''' Determines if a game move is valid or not '''

        
    def __init__( self ):
        my_deck =  Deck()
        my_deck.shuffle()
    
        ''' CREATING THE TABLEAUS AS A DICTIONARY OF LISTS '''

        
                
        #return board_list,tableau_dict
    
    def create_board(my_deck):
        #my_deck =  Deck()
        board_list = []
        tableau_dict = dict()
    
        ''' CREATING THE TABLEAUS AS A DICTIONARY OF LISTS '''

        tableau_list = ['1','2','3','4','5','6','7','Stock','Foundation']
        
        #cards = get_cards()
        for string in tableau_list:
            temp_list = []
            if string in '1234':
                for i in range(7):
                    if i < 3:
                        card = my_deck.deal()
                        card.flip_card()
                        temp_list.append(card)
                    else:
                        temp_list.append(my_deck.deal())
                tableau_dict[string] = temp_list
            elif string in '567':
                for i in range(7):
                    temp_list.append(my_deck.deal())
                tableau_dict[string] = temp_list
            elif string == 'Stock':
                for i in range(3):
                    card = my_deck.deal()
                    card.flip_card()
                    temp_list.append(card)
                tableau_dict[string] = temp_list
            else:
                tableau_dict[string] = temp_list
        
        ## MAKE THE BOARD USING LISTS FROM THE TABLEAU DICT
        for tableau,card in tableau_dict.items():
            if tableau != 'Stock' and tableau != 'Foundation':
                board_list.append(card)
                
        return board_list,tableau_dict     
    
    def write_stats(total_moves,rounds,score,wins):
        average_moves = total_moves//rounds
        HEADER = 'MY STATISTICS'.center(60)
        
        Current_Date_Formatted = datetime.datetime.today().strftime ('%d-%m-%Y %H:%M:%S')
        
        s1 = 'Number of rounds played:  {}'.format(rounds)
        s2 = 'Number of wins:           {}'.format(wins)    
        s3 = 'Total moves:              {}'.format(total_moves)
        s4 = 'Average number of moves:  {}'.format(average_moves)
        fp = open('single.txt', 'a')
        print(HEADER,file=fp)
        print ('Date: ' + str(Current_Date_Formatted),file=fp)
        print(s1,file=fp)
        print(s2,file=fp)
        print(s3,file=fp)
        print(s4,file=fp)
        print('\n\n',file=fp)
        
        fp.close()
                
    def write_stats_main(total_moves,rounds,score,wins):
        average_moves = total_moves//rounds
        Current_Date_Formatted = datetime.datetime.today().strftime ('%d-%m-%Y %H:%M:%S')
        print('\n')
        HEADER = 'MY STATISTICS'.center(60)
        s1 = 'Number of rounds played:  {}'.format(rounds)
        s2 = 'Number of wins:           {}'.format(wins)    
        s3 = 'Total moves:              {}'.format(total_moves)
        s4 = 'Average number of moves:  {}'.format(average_moves)
        s5 = 'Number of losses:         {}'.format(rounds-wins)
        s6 = 'Winning percentage:       {}'.format((wins//rounds)*100)
        fp = open('multiple.txt', 'a')
        print(HEADER,file=fp)
        print('\n',file=fp)
        print ('Date: ' + str(Current_Date_Formatted),file=fp)
        print(s1,file=fp)
        print(s2,file=fp)
        print(s5,file=fp)
        print(s6,file=fp)
        print(s3,file=fp)
        print(s4,file=fp)
        print('\n\n',file=fp)
    
        fp.close()
    
    def wins(score):
        return score//5200
    

class Board ( object ):
    ''' Uses the representation of moves and draws the board '''
    
    def __init__( self ):
        pass

    
    def get_cards():
        mycard =  Card.Deck()
        return mycard.shuffle()
    
    
                
                
    ''' UPDATING THE BOARD '''
    def update_board(board_list):
        for tableau in board_list:
            if len(tableau) != 0:
                if tableau[len(tableau)-1].is_face_up():
                    continue
                else:
                    tableau[len(tableau)-1].flip_card()
                    
    
                    
    
    ''' DRAWING THE BOARD (CAN BE A METHOD IN BOARD CLASS) '''
    def draw_board(board_list,tableau_dict,score,move):
        ''' FINDS THE SIZE OF LONGEST TABLEAU ON THE BAORD '''
        def max_len():
            max_size = 0
            for tableau in board_list:
                size = len(tableau)
                if size > max_size:
                    max_size = size
            return max_size
        max_size = max_len()
        
        fp = open('single.txt', 'a')
        print('\n',file=fp)
        s_card, f_card = '  ', '  '
        print('{}\t\t\t\t\t\t\t\t{}'.format('Stock','Foundation'),file=fp)
        if len(tableau_dict['Stock']) != 0:
            s_card = tableau_dict['Stock'][0]
        if len(tableau_dict['Foundation']) != 0:
            for card in tableau_dict['Foundation']:
                f_card += card
        print('{}\t\t\t\t\t{}'.format(s_card,f_card),file=fp)
        print('\t\t{}\t\t\t{}\t\t\t{}\t\t\t{}\t\t\t{}\t\t\t{}\t\t\t {}'\
              .format('1','  2','  3','  4','  5','  6',' 7'),file=fp)
        for i in range(1,max_size+1): #range(1,x), x is the max_size returned by max_len
            if i != 1:
                print("\n",file=fp)
            print(format(str(i),"3s"),end='   ',file=fp)
            for j in range(7):
                try:
                    print(board_list[j][i-1],end='\t\t\t',file=fp)
                except:
                    print('  ',end='\t\t\t',file=fp)
        if move != None and len(move)==3:
            t1, t2, i = move
            print('\n')
            print('Card at index {} on tableau {} was appended to tableau {}'.\
                  format(i,t2,t1),file=fp)
        print('Score:  {}'.format(score),file=fp)
                    
        print("\n\n\n",file=fp)
        fp.close()
                    

                    
    
    
def main ( ):
    
    seed_integer = input("Please input your random seed integer: ")
    numb_of_games = input("Kindly enter the number of rounds the multi-player will play: ")
                      

    end_round = int(numb_of_games)
    ext_moves = 0
    random.seed(int(seed_integer))
    
    total_moves, score = 0, 0
    my_deck =  Deck()
    my_deck.shuffle()
    Killgame = False
    wins = 0 
    
    
    board_list,tableau_dict = Game.create_board(my_deck)
    
    while not Killgame:
        move = RandomPlayer.find_moves(board_list,tableau_dict)
        score,total_moves,Killgame = RandomPlayer.make_move(move,board_list,tableau_dict,total_moves,score,Killgame)
        Board.update_board(board_list)
        Board.draw_board(board_list,tableau_dict,score,move)
        ext_moves+=1
        

    Game.write_stats(ext_moves,1,score,int(Game.wins(score))) 
    
    ext_moves = 0
    for i in range(end_round):
        total_moves, score = 0, 0
        my_deck =  Deck()
        my_deck.shuffle()
        Killgame = False
        wins = 0 
        
        
        board_list,tableau_dict = Game.create_board(my_deck)
        #Board.draw_board(board_list,tableau_dict)
        
        while not Killgame:
            move = RandomPlayer.find_moves(board_list,tableau_dict)
            score,total_moves,Killgame = RandomPlayer.make_move(move,board_list,tableau_dict,total_moves,score,Killgame)
            Board.update_board(board_list)
            #Board.draw_board(board_list,tableau_dict)
            ext_moves+=1
            
            if Game.wins(score) == 1:
                wins+=1
                
     

    Game.write_stats_main(ext_moves, end_round, score,wins)

    
main()
    


    

