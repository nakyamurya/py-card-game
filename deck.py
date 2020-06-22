import os
import glob
import random
from PIL import Image, ImageTk

class Card:
    def __init__(self, suit, rank, path):
        self.suit = suit
        self.rank = rank
        self.path = path
        self.back = False
        self.path_back = './PNG-cards-1.3/card_back.png'
        self.size = 0.4 # img size to be returned
    
    def __str__(self):
        return str(self.rank) + ' of ' + self.suit

    def getSuit(self):
        return self.suit

    def getRank(self):
        return self.rank

    def setSuit(self, s):
        self.suit = s

    def setRank(self, r):
        self.rank = r
    
    def getImg(self):  # return Img widget
        
        # if self.back == True, card is upside down
        if self.back:
            img_path = self.path_back
        else:
            img_path = self.path
        
        # opens the image
        img = Image.open(img_path)

        # adjust img size
        adj_w = int(img.width * self.size)
        adj_h = int(img.height * self.size)

        # resize the image and apply a high-quality down sampling filter
        img = img.resize((adj_w, adj_h), Image.ANTIALIAS)

        # PhotoImage class is used to add image to widgets, icons etc
        return ImageTk.PhotoImage(img)

class Deck:
    def __init__(self):
        self.carddeck = []
    
    def init(self):
        card_lst = glob.glob('./PNG-cards-1.3/cards/*.png')

        for c in card_lst:
            card = self.decord(c)
            self.carddeck.append(card)
    
    def decord(self, path):
        filename = os.path.basename(path).split('.', 1)[0]
        rank = int(filename.split('_')[0])
        suit = filename.split('_')[2]
        
        return Card(suit,rank,path)
    
    def listup(self):
        print('Total: ' + str(len(self.carddeck)))
        for card in self.carddeck:
            print(card)
    
    def shuffle(self):
        random.shuffle(self.carddeck)
    
    def draw(self, pos=0):
        return self.carddeck.pop(pos)

if __name__ == '__main__':
    d = Deck()
    d.init()
    d.listup()
    d.shuffle()
    d.listup()
