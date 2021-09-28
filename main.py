from tkinter import *
import pandas
BACKGROUND_COLOR = "#B1DDC6"
import random

current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    orignal_data = pandas.read_csv("data/french_words.csv")
    to_learn = orignal_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, card_timer
    current_card = random.choice(to_learn)
    window.after_cancel(card_timer)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card['French'], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    card_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card['English'], fill="white")


def is_known():
    to_learn.remove(current_card)
    updated_data = pandas.DataFrame(to_learn)
    updated_data.to_csv("data/words_to_learn.csv", index=False)

    next_card()



window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
card_timer = window.after(3000, func=flip_card)

# images
check_img = PhotoImage(file="images/right.png")
cross_img = PhotoImage(file="images/wrong.png")
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")


canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# buttons
unknown_button = Button(image=cross_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)
known_button = Button(image=check_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()