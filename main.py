from tkinter import *
from pandas import *
from random import choice
BACKGROUND_COLOR = "#B1DDC6"
image_num = 1
col1_word = ""
col2_word = ""

def change_cardInfo(language , random_word, card_side):
    global image_num, col1_word, col2_word
    if image_num == 1:
        col1_word = random_word
    if image_num == 3:
        image_num = 1
        return 0
    card_canvas.itemconfig(card_image, image=card_side)
    card_canvas.itemconfig(title, text=language)
    card_canvas.itemconfig(word, text=random_word)
    image_num += 1
    posi = list(lang_data[lang_data[col1] == random_word].to_dict()[col2].keys())
    try:
        col2_word = lang_data[lang_data[col1] == random_word].to_dict()[col2][posi[0]]
        window.after(1500, change_cardInfo, col2, col2_word, card_back)
    except IndexError:
        pass
def flip_card():
    change_cardInfo(col1, choice(language_dictonary[col1]), card_front)
def knows():
    if col1_word in language_dictonary[col1]:
        language_dictonary[col1].remove(col1_word)
        print(True)
    if col2_word in language_dictonary[col2]:
        language_dictonary[col2].remove(col2_word)
        print(True)
    new_csv = DataFrame(language_dictonary)
    print(new_csv)
    new_csv.to_csv("language_data.csv", index=False)
    change_cardInfo(col1, choice(language_dictonary[col1]), card_front)

window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50)
window.config(bg=BACKGROUND_COLOR)

lang_data = read_csv("language_data.csv")
lang_data_dict = lang_data.to_dict()
header_column_list = list(lang_data_dict.keys())
col1 = header_column_list[0]
col2 = header_column_list[1]
language_dictonary = {col1: lang_data[col1].to_list(),
                      col2: lang_data[col2].to_list()}

card_front = PhotoImage(file="card_front.png")
card_back = PhotoImage(file="card_back.png")
right_image = PhotoImage(file="right.png")
wrong_image = PhotoImage(file="wrong.png")

card_canvas = Canvas(width=810, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = card_canvas.create_image(410, 270, image=card_front)
title = card_canvas.create_text(400, 150, text="Title", font=("arial", 40, "italic"))
word = card_canvas.create_text(400, 263, text="Word", font=("arial", 60, "bold"))
card_canvas.grid(row=0, column=0, columnspan=2)

rightButton = Button(image=right_image, highlightthickness=0, borderwidth=0, command=knows)
rightButton.grid(row=1, column=0)

wrongButton = Button(image=wrong_image, highlightthickness=0, borderwidth=0, command=flip_card)
wrongButton.grid(row=1, column=1)
flip_card()
window.mainloop()
