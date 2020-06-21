"""Implementation of Snake game using tkinter. Includes a brute-force bot that wins on even board sizes

Usage:
    python3 main.py
"""


from tkinter import *
from PIL.ImageTk import PhotoImage
from PIL import Image

from board import *
from bot_board import BotBoard

using_bot = False


def main():
    """sets up GUI window and initializes board"""
    # initialize window
    my_window = Tk()
    my_window.title("Snake")
    my_window.resizable(width=False, height=False)

    # initialize game board board
    game_frame = Frame(
        my_window, background=GAME_BACKGROUND_COLOR, highlightthickness=0)
    score_label = Label(game_frame, text="Score: 1", font="Roboto 20",
                        background=GAME_BACKGROUND_COLOR, height=1, foreground="WHITE")
    game_board = BotBoard(game_frame, score_label=score_label, background=GAME_BACKGROUND_COLOR,
                          width=GAME_WIDTH, height=GAME_WIDTH, highlightthickness=0) if using_bot else \
        Board(game_frame, score_label=score_label, background=GAME_BACKGROUND_COLOR,
              width=GAME_WIDTH, height=GAME_WIDTH, highlightthickness=0)

    score_label.pack(side=BOTTOM, fill=X)
    game_frame.pack(side=LEFT)

    # initialize menu
    menu_frame = Frame(my_window, background=MENU_COLOR, width=MENU_WIDTH,
                       highlightthickness=1, highlightbackground=BORDER_COLOR)

    menu_placeholder_frame = Frame(
        menu_frame, background=MENU_COLOR, width=MENU_WIDTH, height="150")
    menu_placeholder_frame.pack()

    dimensions_label = Label(menu_frame, text="Dimensions (N x N)",
                             font="Roboto 12 bold", height=1, background=MENU_COLOR)
    dimensions_label.pack()

    entry_frame = Frame(menu_frame, background=MENU_COLOR)
    entry_label = Label(entry_frame, text="N = ",
                        font="Roboto 12 bold", height=1, background=MENU_COLOR,)
    entry_label.pack(side=LEFT)
    entry_field = Entry(entry_frame, font="Roboto 12 bold", width="4")
    entry_field.bind(
        "<Return>", game_board.handle_dimension_change)
    entry_field.pack(side=LEFT)
    entry_frame.pack()

    menu_placeholder_frame_2 = Frame(
        menu_frame, background=MENU_COLOR, width=MENU_WIDTH, height="100")
    menu_placeholder_frame_2.pack()

    play_again_button = Button(menu_frame, text="Play Again",
                               font="Roboto 12 bold", command=game_board.restart_game)
    play_again_button.pack()

    menu_frame.pack(side=LEFT, fill=Y)

    if using_bot:
        my_window.after(1000, game_board.start_bot)
    my_window.mainloop()


main()
