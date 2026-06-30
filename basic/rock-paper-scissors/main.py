# import and global variables
import random
USER_CHOICE = ["rock","paper","scissor"]

# create function to get user input
def get_user_input():
    choice = input("pick your choice ['rock','paper','scissor']:  ")
    while choice not in USER_CHOICE:
        choice = input("pick your choice ['rock','paper','scissor']:  ")
    return choice
# create a function to create pc input
def get_pc_input():
    pc_choice = random.choice(USER_CHOICE)
    print(f"pc choice was {pc_choice}")
    return pc_choice



# compare and determine which one is winner
def winner(user_input , pc_input):
    if user_input == pc_input:
        return "Draw"
    elif (user_input == "rock" and pc_input == "scissor")\
        or (user_input == "scissor" and pc_input == "paper") \
        or (user_input == "paper" and pc_input == "rock"): 
        print("user won!!!!")
    else:
        print("PC won!!!")

# create a main function as runner
def main():
    user_input = get_user_input()
    pc_input = get_pc_input()
    winner(user_input , pc_input)
    print("end of program")

# make an iteration for the game as much as we need
answer = 'y'
while answer == 'y':
    main()
    answer = input("Do you want to continue( y or n ): ")