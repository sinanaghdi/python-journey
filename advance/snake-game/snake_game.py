from tkinter import *
from random import randint

class Snake:
    def __init__(self):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []
        
        for i in range(0, BODY_SIZE):
            self.coordinates.append([0,0])

        for x,y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE , y+SPACE_SIZE,  fill=SNAKE_COLOR , tag='snake' )
            self.squares.append(square)
            
class Food:
    def __init__(self):
        x = randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
        y = randint(0, (GAME_HIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = (x,y)
        canvas.create_rectangle(x, y, x+SPACE_SIZE , y+SPACE_SIZE,  fill=FOOD_COLOR  , tag='Food' )          
            


# def next_turn(snake,food):
    


def restart_program(arg):
    pass
#-------------------------------------------
GAME_WIDTH = 700
GAME_HIGHT = 700
SPACE_SIZE = 25
SLOWNESS = 200
BODY_SIZE = 2
SNAKE_COLOR = "yellow"
FOOD_COLOR = "RED"
BACKGROUND_COLOR = "black"

score = 0
direction = "down"
#------------------------------------------

window = Tk()
window.title("Snake Game")
window.resizable(False,False) 

label = Label(window, text=f"score: {score}",font=("Courier", 30))
label.pack()
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HIGHT , width=GAME_WIDTH)
canvas.pack()

restart = Button(window, text="Restart", fg="red",command=restart_program)
restart.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_height / 2))
y= int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

snake = Snake()
food = Food()


next_turn(snake, food)

window.mainloop()
