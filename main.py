import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont

from PIL import Image, ImageTk
import deck
import player

class SimpleBlackJack(tk.Tk):
    def __init__(self):
        super(SimpleBlackJack, self).__init__()
        self.title("Simple Blackjack")  # Set Title
        self.geometry("{}x{}".format(1000,1000))  # Set the resolution of window
        self.set_valuables()  # initialize valuables
        self.fontStyle = tkFont.Font(  # font setting
            family="Arial",
            size=32,
        )

    def set_valuables(self):
        self.set_board()
        self.set_button()  # place button
        self.deck = self.initDeck()
        self.player = player.Player(self)
        self.enemy = player.Enemy(self)
        self.card_img_p = []
        self.card_img_e = []

        # disable hit button and stand button
        self.btn_hit['state'] = tk.DISABLED
        self.btn_stand['state'] = tk.DISABLED

    def initDeck(self): # get playing card deck
        d = deck.Deck(drop_joker=True, black_jack=True)
        d.init()
        d.shuffle()

        return d
    
    def set_board(self):
        # field
        self.board = tk.Canvas(self, bg='lime green', width=1000, height=1000)
        self.board.place(x=0, y=0)
    
    def set_button(self):
        # game start button
        self.btn_start = tk.Button(
            self,
            text='Start',
            command=self.game_start,
        )
        self.btn_start.place(x=0, y=900)

        # reset button
        self.btn_close = tk.Button(
            self,
            text='Close',
            command=self.close,
        )
        self.btn_close.place(x=100, y=900)

        # clear button
        self.btn_clear = tk.Button(
            self,
            text='Reset',
            command=self.clear,
        )
        self.btn_clear.place(x=200, y=900)

        # hit button
        self.btn_hit = tk.Button(
            self,
            text='Hit',
            command=self.hit,
        )
        self.btn_hit.place(x=300, y=900)

        # stand button
        self.btn_stand = tk.Button(
            self,
            text='Stand',
            command=self.stand,
        )
        self.btn_stand.place(x=400, y=900)
        
    def place_card(self, p):
        # get card image
        # push img data to valuable in this class otherwise img will be discarded by gabage colletion fuction
        
        c = p.get_last_card()
        if p == self.player:
            self.card_img_p.append(c.getImg())
            img = self.card_img_p[-1]
        else:
            self.card_img_e.append(c.getImg())
            img = self.card_img_e[-1]

        # create a label
        self._place_card(
            p.card_pos_x + len(p.hand) * 40,
            p.card_pos_y,
            img,
        )
        # print(self.board.find_all())

    def _place_card(self, x, y, img):
        self.board.create_image(
            x,
            y,
            image=img
        )

    def render_player_numbers(self):
        # render player point
        p_point = tk.Label(
            text=self.player.point,
            foreground='#0000ff',
            background='#00ffff',
            font=self.fontStyle,
            ).place(anchor=tk.CENTER, relx=0.5, rely=0.5, y=0)
    
    def render_enemy_numbers(self):
        # render enemy point
        e_point = tk.Label(
            text=self.enemy.point,
            foreground='#ff0000',
            background='#ffaacc',
            font=self.fontStyle,
            ).place(anchor=tk.CENTER, relx=0.5, rely=0.4, y=0)
        
    def game_end(self, bust=False):
        
        # disable hit button and stand button
        self.btn_hit['state'] = tk.DISABLED
        self.btn_stand['state'] = tk.DISABLED

        # replace enemy card
        self.replace_enemy_card()

        if bust:
            message = 'Bust! Dealer win'
        else:
            message = self._game_end()

        winner_lab = tk.Label(
            text=message,
            foreground='#454545',
            font=self.fontStyle,
        ).place(anchor=tk.CENTER, relx=0.7, rely=0.5)

    def replace_enemy_card(self):

        # delete all enemy's card img
        self.card_img_e = []

        # re-rendering all enemy's card
        i = 1
        for c in self.enemy.hand:
            c.back = False
            self.card_img_e.append(c.getImg())
            img = self.card_img_e[-1]

            # place card
            self._place_card(
                self.enemy.card_pos_x + i * 40,
                self.enemy.card_pos_y,
                img,
            )
            i += 1

    def _game_end(self):
        player_dev = 21 - self.player.point
        enemy_dev = 21 - self.enemy.point

        if self.enemy.point > 21:
            return 'Player win'
        elif (player_dev < enemy_dev):
            return 'Player win'
        elif (player_dev > enemy_dev):
            return 'Dealer win'
        else:
            return 'Draw'

    def game_start(self):
        # draw 2 cards to player
        for i in range(2):
            self.player.push(self.deck.draw())
            self.place_card(self.player)
        
        # draw 2 cards to enemy
        for i in range(2):
            self.enemy.push(self.deck.draw())
            self.place_card(self.enemy)
        
        self.print_points()
        self.render_player_numbers()

        # disable start button
        self.btn_start['state'] = tk.DISABLED

        # enable hit button and stand button
        self.btn_hit['state'] = tk.NORMAL
        self.btn_stand['state'] = tk.NORMAL
    
    def bust_check(self):
        if self.player.point > 21:
            self.game_end(bust=True)

    def hit(self):
        # push card to player
        self.player.push(self.deck.draw())
        self.place_card(self.player)
        self.render_player_numbers()
        self.bust_check()
    
    def stand(self):
        while (self.enemy.point < 17):
            self.enemy.push(self.deck.draw())
            self.place_card(self.enemy)
        self.render_enemy_numbers()
        self.game_end()
    
    def print_points(self):  # print points in console
        # print points in console
        print('Player:{}'.format(self.player.point))
        print('Enemy:{}'.format(self.enemy.point))

    def clear(self):  # initialize
        self.board.delete('all')
        self.set_valuables()

    def remove(self):  # remove card
        self.card_img.pop()

    def close(self):
        self.quit()
    
    def run(self):
        self.mainloop()

if __name__ == '__main__':
    g = SimpleBlackJack()
    g.run()
