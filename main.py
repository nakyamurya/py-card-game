import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont

from PIL import Image, ImageTk
import deck
import player

class Poker(tk.Tk):
    def __init__(self):
        super(Poker, self).__init__()
        self.title("Kusoge")  # Set Title
        self.geometry("{}x{}".format(1000,1000))  # Set the resolution of window
        self.set_valuables() # initialize valuables

    def set_valuables(self):
        self.set_board()
        self.set_button()  # place button
        self.deck = self.initDeck()
        self.player = player.Player()
        self.enemy = player.Enemy()
        self.turn_count = 0
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
        # turn button
        self.btn_turn = tk.Button(
            self,
            text='Next turn',
            command=self.turn,
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
        
    def place_card(self, card, pos_x, pos_y, tag):
        # get card image
        # push img data to valuable in this class otherwise img will be discarded by gabage colletion fuction
        self.card_img.append(card.getImg())

        # create a label
        self.board.create_image(
            pos_x + self.turn_count * 40,
            pos_y,
            image=self.card_img[-1],
            tags = tag
        )
        print(self.board.find_all())


    def render_card(self):
        # render player hand
        self.place_card(
            card=self.player.get_last_card(),
            pos_x=500,
            pos_y=700,
            tag = 'P' + str(self.turn_count)
        )

        # render enemy hand
        self.place_card(
            card=self.enemy.get_last_card(),
            pos_x=500,
            pos_y=200,
            tag='E' + str(self.turn_count)
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
            ).place(anchor=tk.CENTER, relx=0.5, rely=0.7, y=-25)
        
        # render enemy point
        e_point = tk.Label(
            text=self.enemy.point,
            foreground='#ff0000',
            background='#ffaacc',
            font=fontStyle,
            ).place(anchor=tk.CENTER, relx=0.5, rely=0.4, y=20)
        
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

    def turn(self):
        # increment turn
        self.turn_count += 1
        
        # push card to player
        self.player.push(self.deck.draw())

        # push card to enemy
        self.enemy.push(self.deck.draw())

        # render card img in field
        self.render_card()

        # render numbers
        self.render_numbers()

        # determine winner
        if (self.turn_count >= 5):
            self.game_end()
    
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
    g = Poker()
    g.run()
