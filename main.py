from Fast_Words import FastWords
import time
import re


current_text = ''
Fast_bot = FastWords()


while True:
    print("Starting new game!")
    time.sleep(2)
    print(Fast_bot.EndGame(click=True))
    start_time = time.time()
    #time.sleep(3)
    # Plays one Episode
   
    while not Fast_bot.EndGame():

        
        for i in range(25):
            text = Fast_bot.ReadScreen()
            if len(text) > 0 and text != current_text:
                current_text = text
                print(current_text)

             

        # Strip everything but spaces and capitals
        current_text = re.sub(r'[^A-Z] ', '', current_text).rstrip()

        # If we have two words just take the first one
        if len(current_text.split()) > 1:
            current_text = current_text.split()[0]

        # Now kill the spaces.
        current_text = re.sub(r'[^A-Z]', '', current_text)
        print(current_text)

       

        for letter in current_text:
            print(f"Looking for {letter}")
            Fast_bot.find_letter(letter)
            time.sleep(.2)
        time.sleep(2)