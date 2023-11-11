from tkinter import *
import pandas
import random

BACKGROUND_COLOR ="#ECF2FF"
current_word = {}
to_learn = {}

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/korean_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def next_word():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(to_learn)
    canvas.itemconfig(title_card, text="Korean")
    canvas.itemconfig(word_card, text=current_word["Korean"])
    canvas.itemconfig(word_pronunciation, text=current_word["Pronunciation"])
    canvas.itemconfig(background_img, image=front_card_img)
    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(title_card, text="English")
    canvas.itemconfig(word_card, text=current_word["English"])
    canvas.itemconfig(word_pronunciation, text="")
    canvas.itemconfig(background_img, image=back_card_img)

def is_known():
    to_learn.remove(current_word)
    data = pandas.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.csv" , index=False)
    next_word()

window = Tk()
window.title("Korean to English Flashcards")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=420, height=600)
front_card_img = PhotoImage(file="./images/card_front.png")
back_card_img = PhotoImage(file="./images/card_back.png")
background_img = canvas.create_image(210, 300, image=front_card_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title_card = canvas.create_text(210, 200, text="", font=("Arial", 25, "italic"))
word_card = canvas.create_text(210, 300, text="", font=("Arial", 40, "bold"))
word_pronunciation = canvas.create_text(210, 400, text="", font=("Arial", 30, "italic"))
canvas.create_text(210, 510, text="Korean to English", font=("Arial", 20, "italic"))
translation_img = PhotoImage(file="./images/translation.png")
trans_img = canvas.create_image(210, 100, image=translation_img)
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="./images/right.png")
right_btn = Button(image=right_img, command=is_known)
right_btn.config(bg=BACKGROUND_COLOR, highlightthickness=0)
right_btn.grid(row=1, column=0)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(image=wrong_img, command=next_word)
wrong_btn.config(bg=BACKGROUND_COLOR, highlightthickness=0)
wrong_btn.grid(row=1, column=1)

next_word()

window.mainloop()