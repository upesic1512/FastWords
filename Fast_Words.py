import cv2
import mss
import numpy as np
import pytesseract
import pyautogui
import time
import os


class FastWords:
    def __init__(self):
        self.SCT = mss.mss()
        self.dimensions = {
            'left': 750,
            'top': 90,
            'width': 400,
            'height': 100
        }

    def ReadScreen(self, debug=False):
        scr = self.SCT.grab(self.dimensions)
        img = np.array(scr)
        color = cv2.cvtColor(img, cv2.IMREAD_COLOR)

        # Only show if we are debugging
        if debug:
            cv2.imshow("The result", color)
            cv2.waitKey(0)

        path_tess = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = path_tess
        text = pytesseract.image_to_string(color)
        text = text.replace('\x0c', '').replace('[', '')
        if debug:
            if text == '':
                print("Nothing")
        return text
    
    def EndGame(self, click=False, debug=False):
        count = 0
        if count == 0:
            area = {
                'left': 725,
                'top': 915,
                'width': 500,
                'height': 100
            }
            scr = self.SCT.grab(area)
            img = np.array(scr)[:, :, :3]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.uint8) # convert to 8-bit grayscale
            try_again = cv2.imread('TryAgain.png', cv2.IMREAD_GRAYSCALE).astype(np.uint8) # convert to 8-bit grayscale
            result = cv2.matchTemplate(img, try_again, cv2.TM_SQDIFF_NORMED)

            #result = cv2.matchTemplate(img, try_again, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if debug:
                cv2.imshow("slika", img)
                cv2.waitKey()

                print('RRR:')
                print(min_val)
            if min_val < 0.1:
                if click:
                    #print(max_loc[0] + area['left'], max_loc[1] + area['top'])
                    top_adj = max_loc[1] + area['top']
                    left_adj = max_loc[0] + area['left']
                    pyautogui.click(left_adj, top_adj,clicks=2,interval=1)
                    count = 1
                return True
            return False

    def find_letter(self, letter):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(dir_path, f"Letters/{letter}.png")
        area = {
            'left': 500,
            'top': 250,
            'width': 500,
            'height': 600
        }

        max_val = 0
        try_count = 0
        while max_val < .95:
            scr = self.SCT.grab(area)
            img = np.array(scr)[:, :, :3]
            letter = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            result = cv2.matchTemplate(img, letter, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if try_count % 10000 == 0:
                print(max_val)
            # time.sleep(5)
            try_count += 1
            if try_count > 10000 or self.EndGame():
                print("Can't find it")
                time.sleep(5)
                break
        top_adj = max_loc[1] + area['top']+20
        left_adj = max_loc[0] + area['left'] + 5
        pyautogui.click(left_adj, top_adj)

            
       
       

        


if __name__ == "__main__":
    # Testing class
    screen = FastWords()
    screen.find_letter("O")