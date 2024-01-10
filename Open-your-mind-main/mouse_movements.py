import pyautogui
import random
def click_button(x1, x2, y1, y2):

    rand_x = random.randint(x1, x2)
    rand_y = random.randint(y1, y2)


    rand_num = random.randint(0, 3)
    if rand_num == 1:
        movement = pyautogui.easeInQuad
    elif rand_num == 2:
        movement = pyautogui.easeOutQuad
    elif rand_num == 3:
        movement = pyautogui.easeInElastic


    pyautogui.moveTo(rand_x, rand_y, 1, movement)
    pyautogui.click()

def write_amount(num):
    for i in range(10):
        pyautogui.press('delete')
    pyautogui.write(str(num))

if __name__ == '__main__':
    x, y = pyautogui.size()
    x1, y1 = pyautogui.position()
    pyautogui.moveTo(x - 50 , y - 50, 1, pyautogui.easeInElastic)





