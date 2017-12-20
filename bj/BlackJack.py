#!/usr/bin/python
# -*- coding: utf-8 -*

## ☘♣♥♦♠♤♡♢♧☹☺☠

from Deck import Card, Hand, Deck
from Player import Player

class BlackJack(object):
    QM='\n\t?'
    """neg numbers are return codes, positive numbers are parsed values """
    rcLeave=-10
    rcPass=-20
    rcQuit=-90
    rcNo=-128
    rcYes=-127
    
    
    def __init__(self):
        self.name="Py-Eyed Casino"
        self.bank=100000
        self.dealer=Player('dealer',self.bank)
        self.deck=Deck()
        self.deck.shuffle_2()
        self.players=[]
        self.round=0
        self.hands=0
        ss='♤♡♢♧'
        tt=ss
        
        self.HEAD='<*+%s+=== '%(ss)+self.name+' ===+%s+*>'%(ss)

    

    def confirm(self,Q,da=True):
        r=raw_input(Q+BlackJack.QM)
        def dYes(r):
            if r[0] in 'NnFf':
                return False
            return True
        def dNo(r):
            if r[0] in 'YyTt':
                return True
            return False
        if da:
            return dYes(r)
        return dNo(r)
    
    

    def askAnte(self,player):
        """players may ante up $10 or more or Pass or R emove themselves from the game or Quit 
        a positive return value means bet was placed. 
        negative values are return codes and will be processed
        """
        print ('$%s ~ Ante In for $10 Min ~ %s$')%('<'*5,'>'*5)
        print('\tEnter Q to Quit the game or R to remove player')
        q="How much does %s wish to Ante %s$"%(player.name,BlackJack.QM)
        bet=-1
        while bet<0:
            r=raw_input(q)
            try:
                bet=int(r)
                if bet>=10:
                    player.setWager(bet)
                    print ('%')
                    return bet
                else :
                    print ('Don\'t be a cheapo! $%s too low Minium bet is $10'%(bet))
                    print ("Try Again...")
                    bet=-1
                    continue
            except:
                r=r.upper()
                if r=='R':
                    del player
                    return BlackJack.rcLeave
                elif r=='Q':
                    if self.confirm('really quit?'):
                        exit(0)
                elif r=='P':
                    return BlackJack.rcPass 
                else :
                    print ("%s is not a number - try again()"%(r))
        return bet


    def askBet(self,player):
##        print('\tEnter Q to Quit the game or R to remove player')
        
        q=" %s, How much do you wish increase your wager? %s$"%(player.name,BlackJack.QM)
        r=raw_input(q)
        try:
            bet=int(r)
            player.wager+=bet
            print ('%s wages %s'%(player.name,player.wager))
        except:
            print ('No increase')
        return 0
    
    # works
    def askName(self):
        NN=[]
        N=raw_input ("What is your name? %s"%(self.QM))
        if not N:
            N="Player"
        M=N.title()
        m=1
        while M in NN:
            M+="_%s"%(m)
        NN.append(M)
        P=Player(M)
        self.players.append(P)
        return P
    
    #works
    def scoreString(self,player):
        l,h=player.scores()
        s=('%s')%(l)
        if h>l:
            s+=" or %s"%(h)
        return s

    def showBanks(players=None):
        if players==None:
            players=self.players
        for p in players:
            showBank(p)
    
    def showBank(player):
        b='{name} has ${bank} credits'.format(player.name,player.bank)
        print (b)

    def showStats(self, pp=None):
        """shows wins, hands and bank of each player """
        if pp==None:
            pp=self.players
        for p in pp:
            self.showStatus(p)


    def showStatus(self,player):
        s='{name}: won {wins} out of {hands} has %{bank} credits'
        s=s.format(name=player.name, wins=player.wins, hands=player.hands, bank=player.bank )
        print (s)

    # no return
    def askHit(self,player):
        """confirms if player wants a hit, deals card, shows car and score """
        N=player.name
        ss=self.scoreString(player)
        q='{N} has {S}.  Take a Hit? - '        
        while player.scores()[0]<21:
            if self.confirm(q.format(N=player.name,S= self.scoreString(player) ),False):
                player.hit(self.deck.deal())
                ss=self.scoreString(player)
                print ('%s %s'%(player.hand,ss) )
            else:
                break
    
    #works
    def introPlayers(self):
        print (self.HEAD)
        w="Welcome to %s "%(self.name)
        P=self.askName()
        print ('Welcome %s you have $%s credis')%(P.name, P.bank)
        add=True
        while len(self.players)<4:
            add=raw_input("Add another Player?")
            if add.upper() in 'YES': 
                P=self.askName()
                print ('Welcome %s you have $%s credis')%(P.name, P.bank)
            else:
                break
        print ("Set for %s players, Good Luck"%(len(self.players)))
        
    def play(self):
        
        self.round+=1
        dealer=self.dealer
        dealer.hand=Hand()
        deck=self.deck
        players=self.players[:]
        self.showStats(players)
        if len(deck) <len(players)*5:
            deck=Deck()
            self.deck=deck
        #H='<*++=== '+self.name+' ===+*>'
        H=self.HEAD
        print("\t%s hands dealt:%s"%(self.round, self.hands+self.round))
        print('_'*len(H))
        print (H)
        print('-'*len(H))
        
        print ("Players must ante up at least $10 to start. ")
        for p in players:
            p.setWager(0)
            w=self.askAnte(p)
            if w==BlackJack.rcPass:
                players.remove(p)
                continue
            if w==BlackJack.rcLeave:
                players.remove(p)
                self.players.remove(p)
                continue
            if w>0:
                p.hand=Hand()
                p.hands+=1
        
        print ('='*20)
        # first cards
        for p in players:
            if p.wager>0: 
                p.hit(deck.deal())
                print ('%s'%(p))
        dealer.hit(deck.deal())
        print ('%s'%(dealer))

        print ('='*20)
        # second cards
        for p in players:
            p.hit(deck.deal())
            print ('%s'%(p))
        dealer.hit(deck.deal(False))
        print ('%s'%(dealer))

        print ('='*20)
        # increase the wager if feeling lucky
        for p in players:
            w=self.askBet(p)
    
        print ('='*20)
        
        # extra cards...
        for p in players:
            self.askHit(p)
            if p.scores()[0]>21:
                w=p.wager
                self.bank+=w
                p.bank-=w
                p.wager=0
                print('☠ %s Busted at %s Loses $%s'%(p.name, p.scores()[0], w ))
                players.remove(p)

        # Dealer's Turn
        dealer.unhide()
        print ('%s'%(dealer))
        L,H=dealer.scores()
        while L<17:
            dealer.hit(deck.deal())
            vs=self.scoreString(dealer)
            print ('\tDealer: %s for %s '%(dealer.hand, vs) )
            L,H=dealer.scores()
            ### Not sure if this is rule
            if H>17:
                break
        
        DS=L
        if L>21:
            DS=-1
        elif H<22:
            DS=H
        
        WIN='☺ {player} Wins with {score} Wins ${wage}. ☺'
        LOSE='☹ {player} Loses with {score} Loses ${wage}. ☹'
        for p in players:
            w=p.wager
            L,H=p.scores()
            S=L
            if H<22:
                S=H
            #Win
            if S>DS:
                p.bank+=w 
                self.bank-=w
                print(WIN.format(player=p.name, score=S, wage=w))
                p.wins+=1
            #Lose    
            elif S<DS:
                p.bank-=w 
                self.bank+=w
                print(LOSE.format(player=p.name, score=S, wage=w))
            #Draw    
            else : ## not sure... seems like a rip off
                #Safe Tie, player and dealer got max
                if S==21:
                    print ("%s Ties with Dealer at 21"%(p.name))
                    p.wins+=1
                # Tie goes to House if not 21 :( 
                else :
                    p.bank-=w 
                    bank+=w
                    print('%s, Tie goes to the Dealer, % loses $%'%(S, p.name, w))                    

            p.wager=0 #clear 
        
        self.showStats()
        self.showStatus(dealer)
        if self.confirm('Play again?',True):
            self.play()
        print ('you are now leaving %s'%(self.name) )
        print ('Hope you enjoyed playing. ')
        print(self.HEAD)


bj=BlackJack()
bj.introPlayers()
bj.play()    