import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
import database 
from PIL import Image, ImageTk
from random import sample, choice, randint
from scriptaki import flag_names
from database import highscores

# SIZES
POP_UP_WIDTH = 400
POP_UP_HEIGHT = 400
BUTTON_WIDTH = 450
BUTTON_HEIGHT = 300
PADDING_X_BUTTON = 30
PADDING_Y_BUTTON = 30

# COLORS
TITLE_FRAME_COLOR = '#a1a1a1'
GAME_FRAME_COLOR = '#6e545a'
LEADERBOARD_COLOR = '#ba9073'

# FONTS 
TITLE_FONT = ("Maldini", 26, 'bold')
POP_UP_FONT = ("Corbel", 18, 'bold')

global current_score, top_score
current_score=0
top_score=0

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("FLAGUESS")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.attributes("-topmost", True)

        self.window_frame = ctk.CTkFrame(self, height=200,  fg_color=TITLE_FRAME_COLOR, corner_radius=0)
        self.window_frame.grid(row=0, column=0, sticky="ew")
        self.window_frame.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self.window_frame, text=f"You lost. Do you want to exit?\nYour score was {current_score}.\nYour top score was {top_score}.", font = POP_UP_FONT, anchor='center')
        self.label.grid(row=0,column=0, padx=20, pady=20)
        self.label.grid_columnconfigure(0, weight=1)

        self.try_again_button = ctk.CTkButton(self.window_frame, text = "Try Again", command = init_buttons)
        self.try_again_button.grid(row=1, column=0, padx = 15, pady = 15)

        self.quit_button = ctk.CTkButton(self.window_frame, text = "Quit", command = close)
        self.quit_button.grid(row=1, column=1, padx = 15, pady = 15)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("FLAGUESS")
        self.resizable(False, False)
        self.iconbitmap(default='Flags/IconFolder/flag_icon.ico')

        self.toplevel_window = None
        
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)


        # FRAMES
        self.title_frame = ctk.CTkFrame(self, height=200,  fg_color=TITLE_FRAME_COLOR, corner_radius=0)
        self.title_frame.grid(row=0, column=0, sticky="nsew")
        self.title_frame.grid_columnconfigure(0, weight=1)

        self.flag_name_frame = ctk.CTkFrame(self, height=200,  fg_color=TITLE_FRAME_COLOR, corner_radius=0)
        self.flag_name_frame.grid(row=1, column=0, sticky="nsew")
        self.flag_name_frame.grid_columnconfigure(0, weight=1)

        self.game_frame = ctk.CTkFrame(self, height=400, fg_color=GAME_FRAME_COLOR, corner_radius=0)
        self.game_frame.grid(row=2, column=0, sticky="nsew")

        self.leaderboard_frame = ctk.CTkFrame(self, width=150, fg_color=LEADERBOARD_COLOR, corner_radius=0)
        self.leaderboard_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")
        self.leaderboard_frame.grid_rowconfigure(2, weight=1)

        # Game frame widgets
        self.run_button = ctk.CTkButton(self.game_frame, text = "Play", font = TITLE_FONT,width = 150, height = 100, command=self.initialize_buttons)
        self.run_button.grid(row=0,column=0, padx=PADDING_X_BUTTON,pady=PADDING_Y_BUTTON)

        self.score_label = ctk.CTkLabel(self.game_frame, text = "", font = ("Corbel", 36), anchor='center')
        self.score_label.grid(row=0,column=1)
        
        # Title frame widgets
        self.title_label = ctk.CTkLabel(self.title_frame, text = "FLAGUESS", font = TITLE_FONT, anchor='center')
        self.title_label.grid(row=0, column=0, padx=20, pady=20)
        self.title_label.grid_columnconfigure(0, weight=1)

        self.flag_name = ctk.CTkLabel(self.flag_name_frame, text = "Guess the flag", font = TITLE_FONT, anchor='center')
        self.flag_name.grid(row=0, column=0, padx=20, pady=20)
        self.flag_name.grid_columnconfigure(0, weight=1)

        # Leaderboard widgets
        self.leaderboard_label = ctk.CTkLabel(self.leaderboard_frame, text=database.get_leaderboard(highscores, 5), font = ("Corbel", 22, 'bold'), justify='left')
        self.leaderboard_label.grid(row=0,column=0, sticky="ew",padx=10)
        self.leaderboard_label.grid_columnconfigure(0, weight=1)
        self.leaderboard_label.grid_rowconfigure(0, weight=1)


    def make_buttons(self):
        self.button_tl = ctk.CTkButton(self.game_frame, text = "", fg_color = 'transparent', hover_color=TITLE_FRAME_COLOR, width = BUTTON_WIDTH, height = BUTTON_HEIGHT)
        self.button_tl.grid(row=1,column=0, padx=PADDING_X_BUTTON,pady=PADDING_Y_BUTTON)

        self.button_tr = ctk.CTkButton(self.game_frame, text = "", fg_color = 'transparent', hover_color=TITLE_FRAME_COLOR, width = BUTTON_WIDTH, height = BUTTON_HEIGHT)
        self.button_tr.grid(row=1,column=1, padx=PADDING_X_BUTTON,pady=PADDING_Y_BUTTON)

        self.button_bl = ctk.CTkButton(self.game_frame, text = "", fg_color = 'transparent', hover_color=TITLE_FRAME_COLOR, width = BUTTON_WIDTH, height = BUTTON_HEIGHT)
        self.button_bl.grid(row=2,column=0, padx=PADDING_X_BUTTON,pady=PADDING_Y_BUTTON)

        self.button_br = ctk.CTkButton(self.game_frame, text = "", fg_color = 'transparent', hover_color=TITLE_FRAME_COLOR, width = BUTTON_WIDTH, height = BUTTON_HEIGHT)
        self.button_br.grid(row=2,column=1, padx=PADDING_X_BUTTON,pady=PADDING_Y_BUTTON)

        self.button_list = [self.button_tl, self.button_tr, self.button_bl, self.button_br]

    def initialize_buttons(self):
        self.make_buttons()
        self.leaderboard_label.configure(font = ("Corbel", 30, 'bold'))
        self.run_button.configure(state='disabled')
        flags = self.get_flags()

        global correct_flag
        correct_flag = choice(flags)
        flags.remove(correct_flag)

        self.flag_name.configure(text = correct_flag)

        ## h removge apla bgazei thn correct flag apo tis flags opote mporew na kanw apla auto gia na exw tis ypolooipes mesa sto flags
        correct_index = randint(0,3)
        self.button_list[correct_index].configure(image = self.get_flag_image(correct_flag))
        self.button_list[correct_index]['image'] = self.get_flag_image(correct_flag)
        self.button_list[correct_index].configure(command=lambda: self.clicked(correct_flag))

        self.button_list.remove(self.button_list[correct_index])

        for i, button in enumerate(self.button_list):
            button.configure(image=self.get_flag_image(flags[i]))
            button['image'] = self.get_flag_image(flags[i])
            button.configure(command=lambda: self.clicked(flags[i]))


    def get_flag_image(self, flag_name):
        return ctk.CTkImage(light_image=Image.open(f"Flags/flag_{flag_name}.png"), dark_image=Image.open(f"Flags/flag_{flag_name}.png"), size=(BUTTON_WIDTH, BUTTON_HEIGHT))

    def get_flags(self):
        return sample(flag_names, 4)

    def clicked(self, image_flag):
        if image_flag == correct_flag:
            self.initialize_buttons()
            global current_score
            current_score+=1
            self.score_label.configure(text=current_score)

        else:
            check_max()
            self.button_tl.configure(state="disabled")
            self.button_tr.configure(state="disabled")
            self.button_bl.configure(state="disabled")
            self.button_br.configure(state="disabled")
            self.open_toplevel()

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.focus() 
        else:
            self.toplevel_window.focus()  # if window exists focus it

def check_max():
    global current_score, top_score
    if current_score > top_score:
        top_score = current_score

def init_buttons():
    app.initialize_buttons()
    global current_score
    current_score = 0
    app.score_label.configure(text=current_score)
    if (app.toplevel_window.winfo_exists()):
        app.toplevel_window.destroy()

def close():
    player_name = button_click_event()
    database.add_player(player_name, top_score)
    app.destroy()

def button_click_event():
    dialog = ctk.CTkInputDialog(text="Do you want to submit your highscore?\nPut name here.",title="Submit your highscore")
    response = dialog.get_input()
    print("Name of Player:", response)
    return response

if __name__ == "__main__":
    app = App()

    ctk.set_appearance_mode("dark")  

    app.mainloop()

