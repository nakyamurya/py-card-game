import tkinter
from tkinter import filedialog
import tkinter.font as tkFont

from PIL import Image, ImageTk
import deck
import player

class Game:
    def __init__(self):
        self.root = tkinter.Tk()
        self.deck = self.initDeck()
        self.player = player.Player()
        self.enemy = player.Enemy()
        self.turn_count = 0

        # Create buttons and place them into the window
        
        # turn button
        self.btn_turn = tkinter.Button(
            self.root,
            text='Next turn',
            command=self.turn,
        )
        # reset button
        self.btn_close = tkinter.Button(
            self.root,
            text='Close',
            command=self.close,
        )


    def initDeck(self):
        d = deck.Deck()
        d.init()
        d.shuffle()

        return d
    
    def place_card(self, card, relx, rely):
        card_img = card.getImg()
        # create a label
        card_lab = tkinter.Label(self.root, image=card_img)

        # set the image as img
        card_lab.photo = card_img
        card_lab.place(
            anchor=tkinter.N,
            relx=relx,
            rely=rely,
            x = self.turn_count * 40,
        )

    def render_card(self):
        # render player hand
        self.place_card(
            card=self.player.get_last_card(),
            relx=0.5,
            rely=0.7,
        )

        # render enemy hand
        self.place_card(
            card=self.enemy.get_last_card(),
            relx=0.5,
            rely=0.1,
        )

    def render_numbers(self):
        
        #font setting
        fontStyle = tkFont.Font(
            family="Arial",
            size=32,
        )

        # render player point
        p_point = tkinter.Label(
            text=self.player.point,
            foreground='#0000ff',
            background='#00ffff',
            font=fontStyle,
            ).place(anchor=tkinter.CENTER, relx=0.5, rely=0.7, y=-25)
        
        # render enemy point
        e_point = tkinter.Label(
            text=self.enemy.point,
            foreground='#ff0000',
            background='#ffaacc',
            font=fontStyle,
            ).place(anchor=tkinter.CENTER, relx=0.5, rely=0.4, y=20)
        
        # render turn
        turn = tkinter.Label(
            text='Turn = ' + str(self.turn_count),
            foreground='#454545',
            font=fontStyle,
            ).place(anchor=tkinter.CENTER, relx=0.2, rely=0.5)
    
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

        winner_lab = tkinter.Label(
            text=winner,
            foreground='#454545',
            font=fontStyle,
        ).place(anchor=tkinter.CENTER, relx=0.7, rely=0.5)

        # disable turn button
        self.btn_turn["state"] = tkinter.DISABLED

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
    
    def place_button(self):
        self.btn_turn.place(
            anchor=tkinter.CENTER,
            y=20,
            relx=0.5,
            rely=0,
        )

        self.btn_close.place(
            anchor=tkinter.NE,
            relx=1.0,
            rely=0,
        )

    def start(self):
        # Set Title
        self.root.title("Kusoge")
        # Set the resolution of window
        self.root.geometry("1000x1000")
        # Allow Window to be resizable
        self.root.resizable(width=True, height=True)
        # place button
        self.place_button()
        #start Game
        self.root.mainloop()
    
    def close(self):
        self.root.destroy()

if __name__ == '__main__':
    g = Game()
    g.start()
