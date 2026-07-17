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
        canvas.create_rectangle(x, y, x+SPACE_SIZE , y+SPACE_SIZE,  fill=FOOD_COLOR  , tag='food' )          

def next_turn(snake, food):
    global direction, score
    
    x, y = snake.coordinates[0]
    
    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
        
    # اضافه کردن سر جدید
    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE , y + SPACE_SIZE, fill=SNAKE_COLOR, tag='snake')
    snake.squares.insert(0, square)
    
    # بررسی خوردن غذا
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        # حذف دم
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
        
    if check_game_over(snake):
        game_over()
    else:
        window.after(SLOWNESS, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    # جلوگیری از حرکت برعکس
    if new_direction == 'up' and direction != 'down':
        direction = 'up'
    elif new_direction == 'down' and direction != 'up':
        direction = 'down'
    elif new_direction == 'left' and direction != 'right':
        direction = 'left'
    elif new_direction == 'right' and direction != 'left':
        direction = 'right'

def check_game_over(snake):
    x, y = snake.coordinates[0]
    
    # برخورد به دیوار
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HIGHT:
        return True
    
    # برخورد به خود
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('Courier', 40), text=f"GAME OVER! Score: {score}",
                       fill='red', tag="gameover")

def restart_program():
    global score, direction, snake, food
    # پاک کردن همه چیز
    canvas.delete(ALL)
    score = 0
    direction = "down"
    label.config(text=f"Score: {score}")
    
    # ایجاد مار و غذا جدید
    snake = Snake()
    food = Food()
    
    # شروع مجدد بازی
    window.after(100, next_turn, snake, food)

#-------------------------------------------
GAME_WIDTH = 700
GAME_HIGHT = 700
SPACE_SIZE = 25
SLOWNESS = 200
BODY_SIZE = 2
SNAKE_COLOR = "yellow"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

score = 0
direction = "down"
#------------------------------------------

window = Tk()
window.title("Snake Game")
window.resizable(False,False) 

label = Label(window, text=f"Score: {score}", font=("Courier", 30))
label.pack()
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HIGHT , width=GAME_WIDTH)
canvas.pack()

restart = Button(window, text="Restart", fg="red", command=restart_program)
restart.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# اتصال کلیدها
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = Food()

# شروع بازی با تاخیر
window.after(100, next_turn, snake, food)

window.mainloop()