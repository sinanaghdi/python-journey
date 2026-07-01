import random

# Global variables
BINGO_SIZE = 5
MIN_NUM = 1
MAX_NUM = 75

# Create a bingo card with random numbers
def create_bingo_card():
    card = []
    used_numbers = set()
    
    for row in range(BINGO_SIZE):
        current_row = []
        for col in range(BINGO_SIZE):
            # Center cell is FREE
            if row == 2 and col == 2:
                current_row.append("FREE")
            else:
                # Generate unique random number
                while True:
                    num = random.randint(MIN_NUM, MAX_NUM)
                    if num not in used_numbers:
                        used_numbers.add(num)
                        current_row.append(num)
                        break
        card.append(current_row)
    
    return card

# Display the bingo card
def display_card(card, marked):
    print("\n" + "=" * 30)
    print("🎱 YOUR BINGO CARD 🎱")
    print("=" * 30)
    
    for row in range(BINGO_SIZE):
        row_str = ""
        for col in range(BINGO_SIZE):
            cell = card[row][col]
            if marked[row][col]:
                row_str += f"[{str(cell):>4}]"
            else:
                row_str += f" {str(cell):>4} "
        print(row_str)
    print("=" * 30 + "\n")

# Check if there's a bingo (complete row, column, or diagonal)
def check_bingo(marked):
    # Check rows
    for row in range(BINGO_SIZE):
        if all(marked[row]):
            return True, f"Row {row + 1}"
    
    # Check columns
    for col in range(BINGO_SIZE):
        if all(marked[row][col] for row in range(BINGO_SIZE)):
            return True, f"Column {col + 1}"
    
    # Check diagonals
    if all(marked[i][i] for i in range(BINGO_SIZE)):
        return True, "Main diagonal"
    
    if all(marked[i][BINGO_SIZE - 1 - i] for i in range(BINGO_SIZE)):
        return True, "Anti-diagonal"
    
    return False, None

# Mark a number on the card
def mark_number(card, marked, number):
    for row in range(BINGO_SIZE):
        for col in range(BINGO_SIZE):
            if card[row][col] == number:
                marked[row][col] = True
                return True
    return False

# Main game function
def main():
    print("🎉 Welcome to BINGO! 🎉")
    print(f"Numbers range: {MIN_NUM} to {MAX_NUM}")
    print("Goal: Complete a row, column, or diagonal to win!\n")
    
    # Initialize game
    card = create_bingo_card()
    marked = [[False for _ in range(BINGO_SIZE)] for _ in range(BINGO_SIZE)]
    
    # Mark FREE space
    marked[2][2] = True
    
    # Generate list of numbers to be called
    called_numbers = list(range(MIN_NUM, MAX_NUM + 1))
    random.shuffle(called_numbers)
    
    display_card(card, marked)
    
    # Game loop
    for number in called_numbers:
        input(f"Press Enter to draw next number...")
        print(f"\n🎲 Number called: {number}")
        
        # Ask player if they want to mark it
        if mark_number(card, marked, number):
            choice = input(f"Number {number} is on your card! Mark it? (y/n): ").lower()
            if choice == 'y':
                mark_number(card, marked, number)
                print(f"✅ Marked {number}")
        else:
            print(f"❌ Number {number} is not on your card")
        
        display_card(card, marked)
        
        # Check for bingo
        has_bingo, winning_line = check_bingo(marked)
        if has_bingo:
            print(f"\n🎊 BINGO! You won with {winning_line}! 🎊")
            break
    else:
        print("\n😔 Game over! No more numbers to call.")
    
    play_again = input("\nPlay again? (y/n): ").lower()
    if play_again == 'y':
        main()
    else:
        print("Thanks for playing! 👋")

# Standard way to run
if __name__ == "__main__":
    main()
    
    
