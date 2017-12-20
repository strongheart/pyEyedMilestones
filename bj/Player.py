# -*- coding: utf-8 -*

from Deck import Card, Hand, Deck

class Player(object):
    def __init__(self, name="Player",bank=1000) :
        self.name=name
        self.bank=bank
        self.hand=Hand()
        self.wager=0
        self.wins=0
        self.hands=0
        self.busted=False
        self.out=False
        self.skip=False

    def getHand(self):
        return self.hand

    def setName(self, name):
        self.name=name
    
    def getName(self):
        return self.name
    
    def getBank():
        return self.bank
    
    def hit(self,card):
        self.hand.hit(card)
    
    def hasAce(self) :   
        '''return 0 no aces 1 if at least one ace (only 1 high ace can count) '''
        for c in self.hand.get():
            if c.isAce():
                return 1
        return 0
    
    def scores(self):
        """return tupple (low score,high score) high score =lowscore+10*hasAce() """
        s=0
        for c in self.hand.get():
            if c.isFaceDown():
                continue
            s+=c.getValue() 
        return [s, s+10*self.hasAce()]

    def getWager(self):
        return self.wager
    
    def setWager(self, w):
        self.wager=w
    
    def addBet(self, bet):
        self.wager+=bet
    
    def win(self, w=None):
        if w==None:
            w=self.wager
        self.bank+=w
    
    def lose(self, w=None):
        if w==None:
            w=self.wager
        self.bank-=w
    
    def __repr__(self):
        N=self.name
        B=' $%s '%(self.bank)
        H=' %s '%(self.hand)
        W='%s'%(self.wager)
        l,h=self.scores
        S='scores:(%s %s) '%(l,h)
        #return 'Player: %s, %s %s %s %s'%(N,B,W, H, S)
        return  'Player: {n}, {b} {w} {h} {a}'.format(n=N,b=B,w=W, h=H, s=S)
    
    def __str__(self):
        ss=self.scores()
        s=str(ss[0]) 
        if ss[0] != ss[1]:
            if ss[1]<=21:
                s+=' or '+str(ss[1])
        return "%s: %s %s bet=%s"%(self.name, str(self.hand), s, str(self.wager))
    
    def unhide(self):
        for c in self.hand.get():
            c.show(True)
    
    def clear(self):
       pass 
    










