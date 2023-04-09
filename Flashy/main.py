from tkinter import *
import random
import pandas

# -------------------- Constants/Variables -------------------- #
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

# -------------------- Remove Word -------------------- #
def remove_word():
    """Removes words from the dictionary that the user knows"""
    words_to_learn.remove(current_card)
    new_data = pandas.DataFrame(words_to_learn)
    new_data.to_csv("/workspaces/hpdowning.github.io/Flashy/data/new_words.csv", index=False)
    next_card()


# -------------------- Change Word -------------------- #
def next_card():
    """Changes the card shown"""
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    canvas.itemconfig(card, image=card_front_img)
    canvas.itemconfig(language, text="Spanish", fill="black")
    canvas.itemconfig(current_word, text=current_card["Spanish"], fill="black")
    flip_timer = window.after(3000, flip_card)

# -------------------- Change Word -------------------- #
def flip_card():
    """Flips the card from the Spanish word to the English equivalent"""
    canvas.itemconfig(card, image=card_back_img)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(current_word, text=current_card["English"], fill="white")


# -------------------- Read CSV -------------------- #
try:
    data = pandas.read_csv("Flashy/data/words-to-learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("Flashy/data/new_words.csv")
    words_to_learn = data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")

# -------------------- UI -------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

# Canvases
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="Flashy/images/card_front.png")
card_back_img = PhotoImage(file="Flashy/images/card_back.png")
card = canvas.create_image(400, 263, image=card_front_img)
language = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
current_word = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))

# Buttons
wrong_img = PhotoImage(file="Flashy/images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0,
                      highlightbackground=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(row=1, column=0)
right_img = PhotoImage(file="Flashy/images/right.png")
right_button = Button(image=right_img, highlightthickness=0,
                      highlightbackground=BACKGROUND_COLOR, command=remove_word)
right_button.grid(row=1, column=1)

canvas.grid(row=0, column=0, columnspan=2)

next_card()

window.mainloop()
