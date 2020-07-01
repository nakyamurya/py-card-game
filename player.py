class PlayerBase:
    def __init__(self, parent):
        self.hand = []
        self.point = 0
        self.parent = parent  # assign SimpleBlackJack class to handle valuables
        self.card_pos_x = None
        self.card_pos_y = None
    
    def push(self, card):
        self.hand.append(card)
        self.point += card.rank
    
    def count_card(self):
        return len(self.hand)
    
    def get_last_card(self):
        return self.hand[-1]

class Player(PlayerBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.card_pos_x = 500
        self.card_pos_y = 700

class Enemy(PlayerBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.card_pos_x = 500
        self.card_pos_y = 200

    # override
    def push(self, card):
        if len(self.hand) == 1:
            card.back = True
        else:
            card.back = False
        self.hand.append(card)
        self.point += card.rank
