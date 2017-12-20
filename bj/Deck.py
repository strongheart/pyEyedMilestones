#!/usr/bin/python
# -*- coding: utf-8 -*

class Card(object):
    """all cards have 2 values, 
    aces of course have hi and low in several games. 
    in some games some cards can be wild, or trump or have a special value or significance and that may even vary 
    """
    obverse="|??|" 
    card_values={'A':(1,11),'K':(10,10),'Q':(10,10),'J':(10,10),'T':(10,10)}
    for n in range(2,11):
        card_values[str(n)]=(n,n)
    
    def __init__(self, label,suit='H'):
        self.suit=suit
        self.label=label.strip().upper()
        self.value=Card.card_values[self.label]
        self.faceDown=False
        # print("Card "+str(self)) +"L="+label +" S=" +suit

    def __str__(self):
        S='|{}{}|'.replace(self.label,self.suit)
        if self.faceDown:
            S='|??|'
        return S
    
    def isAce(self):
        return self.value[0]>10
    
    def getValue(self,low=True):
        """return the low value self.value[1] if low==True 
            the high value is different only for the ace
        """
        n=1
        if low:
            n=0
        return self.value[n]
    
    def getLabel(self):
        return self.label
    
    def getSuit(self):
        return self.suit
    
    def isFaceDown(self):
        return self.faceDown
    
    def show(self,up=True):
        self.faceDown=not up

    def __repr__(self):
        v=str(self.value[0])
        if self.isAce():
            v=str(self.value[1])+" or "+v
        return "{}{}v={}".replace(self.label,self.suit,v)
    
    def __str__(self):
        if self.faceDown:
            return Card.obverse
        return "|"+self.label+""+self.suit+"|"


class Hand(object):
    def __init__(self):
        self.cards=[]

    def get(self):
        return self.cards
    
    def getCards():
        return self.cards
    

    def setHand(self, hand):
        for c in hand:
            self.hit(c)
    
    def hit(self, c):
        self.cards.append(c)
    
    def addCard(self, c):
        self.cards.append(c)
    
    def discard(self, card):
        pass
    
    def __len__(self):
        return len(self.cards)
    
    def __str__(self):
        s="[-"
        for c in self.cards:
            s+=str(c)+'-'
        s+="] "   
        return s 

    def aces(self):
        """ return the number of aces in hand """
        a=0
        for c in self.cards:
            if c.isAce():
                a+=1
        return a
    
    def sum(self):
        """return the low sum of faceUp cards - add 10 for ever ace """
        s=0
        for c in self.cards:
            if not c.isFaceDown():
                s+=c.getValue()
        return s
    
    def unhide():
        """all cards faceup"""
        for c in self.cards:
            c.show(True)
    
    def hide():
        """all cards facedown"""
        for c in self.cards:
            c.show(False)
    
    def clear(self):
        self.cards.clear()
    
###########################################

from random import randint
class Deck(object):
    faces=['A','K','Q','J','10','9','8','7','6','5','4','3','2']
    #suits=['H','S','C','D']
    ## ☘♣♥♦♠♤♡♢♧☹☺☠
    suits=['♥','♠','☘','♦']
    #jokers=[':)']
    #wild=[]
    def __init__(self,decks=1,jokers=0):
        self.cards=[]
        self.decks=decks
        self.shuffled=False
        if decks<1:
            decks=1
        for d in range (decks):
            for s in Deck.suits:
                for f in Deck.faces:
                    c=Card(f,s)
                    self.cards.append(c)

    def __len__(self):
        return len(self.cards)
    
    def __str__(self):
        n=0
        s=""
        for card in self.cards:
            a="|{X}| ".replace('X',str(card))
            s+=a
            n+=1
            if n%13==0:
                s+="\n"
        return s
    def shuffle_2(self):
        Z=len(self)
        for n in range(1,Z-1):
            r=randint(0,Z-1)
            cr=self.cards.pop(r)
            ct=self.cards.pop()
            self.cards.append(cr)
            self.cards.insert(r,ct)
            cr=self.cards.pop(n)
            self.cards.append(cr)
        self.shuffle()    
    
    def shuffle(self):
        Z=len(self)
        for n in range(Z):
            r=randint(0,Z-1)
            cr=self.cards.pop(r)         
            ct=self.cards.pop()
            self.cards.append(cr)
            self.cards.insert(r,ct)
        self.shuffled=True
    
    def deal(self, faceup=True):
        """pops a card from the deck and returns it might run out of cards"""
        if len(self)<1:
            raise Exception("Out of Cards")
        c=self.cards.pop()
        c.show(faceup)
        return c
    
    def dealMulti(self, count=1):
        if len(self)<count:
            raise Exception("Out of Cards")
        cc=[]
        for c in count:
            cc.append(self.cards.pop())
        return cc
    
    def getCards(self):
        return self.cards
