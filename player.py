class PlayerBase:
    def __init__(self):
        self.hand = []
        self.point = 0
    
    def push(self, card):
        self.hand.append(card)
        self.point += card.rank
    
    def count_card(self):
        return len(self.hand)
    
    def get_last_card(self):
        return self.hand[-1]

class Player(PlayerBase):
    pass

class Enemy(PlayerBase):
    # override
    def push(self, card):
        card.back = True
        self.hand.append(card)
        self.point += card.rank