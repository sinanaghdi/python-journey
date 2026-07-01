# global variable and imports


# getting user input as height and weight

def get_user_input():
    weight = float(input("Enter your weight(K): "))
    height = float(input("Enter your height(M): "))
    return weight,height
    

# calculate bmi
def calculate_bmi(weight,height):
    return  weight / (height**2)

# get bmi result
def get_bmi_result(bmi):
    if bmi < 18.5:
        print("Under weight")
    elif 18.5<bmi<25:
        print("Normal")
    elif 25<bmi< 30:
        print("overweight")
    elif 30<=bmi< 35:
        print("obese")
    else:
        print("Extremely obese")
        


# create main function to run
def main():
    weight, height =  get_user_input()
    bmi = calculate_bmi(weight,height)
    get_bmi_result(bmi)
    
    
main()