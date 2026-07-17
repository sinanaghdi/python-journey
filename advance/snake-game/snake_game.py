from tkinter import *


def restart_program(arg):
    pass
#-------------------------------------------
GAME_WIDTH = 700
GAME_HIGHT = 700
SPACE_SIZE = 30
SLOWNESS = 200
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
window.mainloop()
