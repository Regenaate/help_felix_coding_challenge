import os

def main():

    slow_print("So you’re a therapist, and your client (Felix) wants your help on how to achieve his goals. Felix has 3 goals, and you must help him achieve each of them.")
    input("Enter to continue...")  # waits for user input
    os.system('clear')  # clears the terminal on Mac/Linux
    slow_print("His goals are simple. He wants to get a girlfriend for support & companionship. He wants to get better at his job selling life insurance so he can earn more cash, and he wants to overcome his paranoia of believing that some people are secretly shapeshifting reptilians that are currently plotting for humanity’s demise.")

import sys
import time

def slow_print(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if(char == '.'):
            time.sleep(0.8)
        elif(char == ','):
            time.sleep(0.3)
        else:
            time.sleep(0.05)  # Adjust the delay (in seconds) as needed
    print()  # Add a newline at the end



if __name__ == "__main__":
    main()

# game class? Have the game be a graph? 