import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont

from PIL import Image, ImageTk
import deck
import player

class SimpleBlackJack(tk.Tk):
    def __init__(self):
        super(SimpleBlackJack, self).__init__()
        self.title("Kusoge")  # Set Title
        self.geometry("{}x{}".format(1000,1000))  # Set the resolution of window
        self.set_valuables() # initialize valuables

    def set_valuables(self):
        self.set_board()
        self.set_button()  # place button
        self.deck = self.initDeck()
        self.player = player.Player(self)
        self.enemy = player.Enemy(self)
        self.card_img = []

    def initDeck(self): # get playing card deck
        d = deck.Deck()
        d.init()
        d.shuffle()

        return d
    
    def set_board(self):
        # field
        self.board = tk.Canvas(self, bg='lime green', width=1000, height=1000)
        self.board.place(x=0, y=0)
    
    def set_button(self):
        # game start button
        self.btn_turn = tk.Button(
            self,
            text='Start',
            command=self.game_start,
        )
        self.btn_turn.place(x=0, y=750)
        # reset button
        self.btn_close = tk.Button(
            self,
            text='Close',
            command=self.close,
        )
        self.btn_close.place(x=100, y=750)
        # clear button
        self.btn_clear = tk.Button(
            self,
            text='Reset',
            command=self.clear,
        )
        self.btn_clear.place(x=200, y=750)
        # remove button
        self.btn_remove = tk.Button(
            self,
            text='Remove',
            command=self.remove,
        )
        self.btn_remove.place(x=300, y=750)
        
    def place_card(self, card, pos_x, pos_y):
        # get card image
        # push img data to valuable in this class otherwise img will be discarded by gabage colletion fuction
        self.card_img.append(card.getImg())

        # create a label
        self.board.create_image(
            pos_x,
            pos_y,
            image=self.card_img[-1],
        )
        # print(self.board.find_all())


    def render_card(self, p):
        # render card img
        self.place_card(
            card=p.get_last_card(),
            pos_x=p.card_pos_x + len(p.hand) * 40,
            pos_y=p.card_pos_y,
        )

    def render_numbers(self):
        
        #font setting
        fontStyle = tkFont.Font(
            family="Arial",
            size=32,
        )

        # render player point
        p_point = tk.Label(
            text=self.player.point,
            foreground='#0000ff',
            background='#00ffff',
            font=fontStyle,
            ).place(anchor=tk.CENTER, relx=0.5, rely=0.5, y=0)
        
        # render enemy point
        e_point = tk.Label(
            text=self.enemy.point,
            foreground='#ff0000',
            background='#ffaacc',
            font=fontStyle,
            ).place(anchor=tk.CENTER, relx=0.5, rely=0.4, y=0)
        
        # render turn
        turn = tk.Label(
            text='Turn = ' + str(self.turn_count),
            foreground='#454545',
            font=fontStyle,
            ).place(anchor=tk.CENTER, relx=0.2, rely=0.5)
    
    def game_end(self):
        #font setting
        fontStyle = tkFont.Font(
            family="Arial",
            size=32,
        )

        # render player point
        if (self.player.point > self.enemy.point):
            winner = 'Player win'
        elif (self.player.point < self.enemy.point):
            winner = 'Com win'
        else:
            winner = 'Draw'

        winner_lab = tk.Label(
            text=winner,
            foreground='#454545',
            font=fontStyle,
        ).place(anchor=tk.CENTER, relx=0.7, rely=0.5)

        # disable turn button
        self.btn_turn["state"] = tk.DISABLED

    def game_start(self):
        # draw 2 cards to player
        for i in range(2):
            self.player.push(self.deck.draw())
            self.render_card(self.player)
        
        # draw 2 cards to enemy
        for i in range(2):
            self.enemy.push(self.deck.draw())
            self.render_card(self.enemy)
        
        self.print_points()

    def turn(self):
        
        # push card to player
        self.player.push(self.deck.draw())

        # push card to enemy
        self.enemy.push(self.deck.draw())

        # render card img in field
        self.render_card()

        # render numbers
        # self.render_numbers()

        # determine winner
        #if (self.turn_count >= 5):
        #    self.game_end()
    
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
