"""
Resources
Naminf Convention - https://namingconvention.org/python/
Human like mouse movement https://youtu.be/RR8w6SC06cc - mouse dragging movement is generated, reduce coordinates needed to save when dragging
Tkinter https://pythonguides.com/python-tkinter-mainloop/ - updates a window by destroying and reopening it
https://stackoverflow.com/questions/21592630/why-do-my-tkinter-widgets-get-stored-as-none - creating widgets (buttons) correctly

GUI for Mouse Macro
"""


import tkinter as tk
from tkinter import ttk
import pyautogui
from threading import Thread
import macrorecorder
import re
from pathlib import Path
import os


# Functions
def on_closing_root():  # when exiting root GUI, ends threads, destroys all windows
    macrorecorder.end_listener()
    global gui_is_running
    gui_is_running = False
    root.destroy()
    cursor_follow_window.destroy()
    edit_window.destroy()
    input_window.destroy()
    print("Main - Program Ended (Closed)")


def on_closing_input_window():  # when exiting input_window GUI, only hides the window and shows root window
    title1 = tk.Label(
        input_window,
        text="Name your macro \n(Only letters and numbers allowed)",
        background="#252527",
        fg="white",
    ).grid(column=0, row=0, padx=(10, 10), pady=(10, 10))
    inputbox.delete(0, "end")
    root.deiconify()  # makes window appear if it was withdrawn
    input_window.withdraw()  # remove window from screen


def on_closing_edit_window():
    description_one.config(text="Pixel Disposition (0-20 pixel difference)",fg = "white")
    description_two_start.config(text="Random Time Delay Per Press", fg = "white")
    description_two_end.config(fg = "white")
    description_three.config(text="Random Run Chance Percentage (0-100)",fg = "white")
    description_four.config(text="Amount of times repeated (1-10)",fg = "white")
    macro_box_one.focus_set()
    root.deiconify()
    edit_window.withdraw()


def edit_macro():  # only shows edit_window when macro is selected
    if str(macro_list_box.curselection()) != "()":
        global edit_macro_file_name
        edit_macro_file_name = macro_list_box.get(macro_list_box.curselection())
        fullfilepath = (
            str(Path(__file__).parent.resolve())
            + "\macrolist\\"
            + edit_macro_file_name
        )
        print(fullfilepath)
        if Path(fullfilepath).is_file():
            with open(fullfilepath, "r") as file:
                data = file.readlines()
            macro_box_one.delete(0, tk.END)
            macro_box_two_start.delete(0, tk.END)
            macro_box_two_end.delete(0, tk.END)
            macro_box_three.delete(0, tk.END)
            macro_box_four.delete(0, tk.END)

            macro_box_one.insert(0, int(data[0]))
            macro_box_two_start.insert(0, int(data[1]))
            macro_box_two_end.insert(0, int(data[2]))
            macro_box_three.insert(0, int(data[3]))
            macro_box_four.insert(0, int(data[4]))
            macro_box_one.focus_set()
            root.withdraw()
            edit_window.deiconify()
            
    refresh_root_macro_list()
    print("Main - Edit Macro")


def edit_macro_submit():  # changes selected macro's parameters
    pixel_disposition_input = macro_box_one.get()
    delay_start_input = macro_box_two_start.get()
    delay_end_input = macro_box_two_end.get()
    run_chance_input = macro_box_three.get()
    repeat_input = macro_box_four.get()

    isvalid_inputs = True
    
    description_one.config(text="Pixel Disposition (0-20 pixel difference)",fg = "white")
    description_two_start.config(text="Random Time Delay Per Press", fg = "white")
    description_two_end.config(fg = "white")
    description_three.config(text="Random Run Chance Percentage (0-100)",fg = "white")
    description_four.config(text="Amount of times repeated (1-10)",fg = "white")
    
    if not (is_int(pixel_disposition_input) and int(pixel_disposition_input) >= 0 and int(pixel_disposition_input) <= 20):
        description_one.config(text="Pixel Disposition (0-20 pixel difference) INVALID", fg = "red")
        isvalid_inputs = False
    if not (is_int(delay_start_input) and is_int(delay_end_input) and int(delay_start_input)>=0 and int(delay_start_input)<=100 and int(delay_end_input)>=0 and int(delay_end_input)<=100 and int(delay_end_input)-int(delay_start_input)>=0):
        description_two_start.config(text="Random Time Delay Per Press INVALID",fg = "red")
        description_two_end.config(fg = "red")
        isvalid_inputs = False
    if not (is_int(run_chance_input) and int(run_chance_input)>=0 and int(run_chance_input)<=100):
        description_three.config(text="Random Run Chance Percentage (0-100) INVALID", fg = "red")
        isvalid_inputs = False
    if not (is_int(repeat_input) and int(repeat_input)>=1 and int(repeat_input)<=10):
        description_four.config(text="Amount of times repeated (1-10) INVALID", fg = "red")
        isvalid_inputs = False


    if isvalid_inputs:
        print("Main - Valid Macro Sumbit")
        global edit_macro_file_name
        fullfilepath = (str(Path(__file__).parent.resolve()) + "\macrolist\\" + edit_macro_file_name)
        with open(fullfilepath, "r") as file:
            data = file.readlines()
        data[0] = pixel_disposition_input+"\n"
        data[1] = delay_start_input+"\n"
        data[2] = delay_end_input+"\n"
        data[3] = run_chance_input+"\n"
        data[4] = repeat_input+"\n"
        with open(fullfilepath, "w") as file:
            file.writelines(data)
        macro_box_one.focus_set()
        root.deiconify()
        edit_window.withdraw()
    else:
        print("\npixel_disposition_input: " + pixel_disposition_input)
        print("delay_start_input: " + delay_start_input)
        print("delay_end_input: " + delay_end_input)
        print("run_chance_input: " + run_chance_input)
        print("repeat_input: " + repeat_input+"\n")
        
    print("Main - Edit Macro Sumbit")

def is_int(x): # HELPER
    try:
        x = int(x)
        return True
    except:
        return False

def record():  # Records mouse clicks, record button becomes red color, activates record notification window
    global is_recording
    if is_recording == False:  # no dupe buttons/actions when pressed twice
        is_recording = True
        macrorecorder.record_mouse()
        # changes button appearance when enabled
        record_macro_button.config(text="   Recording    ", fg="red")
        cursor_follow_window.attributes("-topmost", True)  # topmost window
        cursor_follow_window.deiconify()
        record_notification()
        print("Main - Record")


def end_record():  # Stops recording mouse clicks, requests user input to export macro, record button becomes black color, removes record notification window
    global is_recording
    if is_recording:
        is_recording = False
        macrorecorder.stop_record_mouse()
        if macrorecorder.valid_macro_list():
            export_macro_window()
        # changes button appearance when disabled
        record_macro_button.config(text="Record Macro", fg="black")
        cursor_follow_window.attributes("-topmost", False)
        cursor_follow_window.withdraw()
        print("Main - End Record")


def export_macro():  # depending on valid user input in export window, file will be created with user input name, and the recorded actions of the mouse
    userinput = inputbox.get()
    if re.match(
        "^[A-Za-z0-9]+[^\s]*$", userinput
    ):  # regex, only alphanumeric string is allowed with no whitespace or empty string, re.match() returns a match object
        title1 = tk.Label(
            input_window,
            text="Name your macro \n(Only letters and numbers allowed)",
            background="#252527",
            fg="white",
        ).grid(column=0, row=0, padx=(10, 10), pady=(10, 10))
        print("Main - Valid User Input")
        macrorecorder.export_mouse_macro(
            userinput
        )  # file is written with file name as 'userinput'
        refresh_root_macro_list()
        root.deiconify()
        input_window.withdraw()
        inputbox.delete(0, "end")  # clears input box range from 0-end
    else:
        title1 = tk.Label(
            input_window,
            text="Invalid Input \n(Only letters and numbers allowed)",
            background="#252527",
            fg="red",
        ).grid(column=0, row=0, padx=(10, 10), pady=(10, 10))
        print("Main - Invalid User Input")


def export_macro_window():  # HELPER shows export window to ask user for input after ending a recording
    root.withdraw()
    input_window.deiconify()
    inputbox.focus_set()  # keyboard focus is on the text field


def refresh_root_macro_list():  # HELPER refresh macro list in root window
    global list_of_macros
    global macro_list_box
    list_of_macros = os.listdir(str(Path(__file__).parent.resolve()) + "\macrolist")
    macro_list_box.delete(0,tk.END)
    for macro in list_of_macros:
        if macro[-4:] == ".txt":
            macro_list_box.insert("end", macro)


def move_Window(
    root_variable, x, y
):  # HELPER used to position record notification window
    root_variable.geometry("+{0}+{1}".format(x, y))
    # print("Main - Moved")


def record_notification():  # HELPER used to constantly update position of record notification window, following mouse position
    if is_recording:
        coordinates = (
            pyautogui.position()
        )  # current mouse position as array [x,y] coordinates
        global current_mouse_position_x, current_mouse_position_y
        current_mouse_position_x = coordinates[0]
        current_mouse_position_y = coordinates[1]
        move_Window(
            cursor_follow_window,
            current_mouse_position_x + 10,
            current_mouse_position_y + 10,
        )
        coord_label = tk.Label(
            cursor_follow_window,
            text="Recording X: {0} Y: {1}".format(
                current_mouse_position_x, current_mouse_position_y
            ),
        ).grid(column=0, row=0)
        cursor_follow_window.after(
            20, record_notification
        )  # loops method every 20ms if recording to follow the mouse
        # print("Main - Running Notification")
    else:
        print("Main - End Notification")


if __name__ == "__main__":
    print("Path of the script: " + str(Path(__file__).parent.resolve()))
    print("Path of the working directory: " + str(Path().resolve()))
    
    # Variables
    gui_is_running = True
    is_recording = False
    current_mouse_position_x = 0
    current_mouse_position_y = 0
    macro_thread = Thread(target=macrorecorder.start_listener)
    macro_thread.start()  # mouse listener thread starts in this thread
    edit_macro_file_name = None
    
    # Main Window
    root = tk.Tk()
    root.title("Mouse Macro")
    root.geometry("400x600")
    root.config(background="#252527")
    root.resizable(width=False, height=False)
    # Title
    title1 = tk.Label(
        root, text="Options", background="#252527", font=("Arial", 15), fg="white"
    ).grid(column=0, row=0, padx=(10, 10), pady=(10, 10))
    # Options for Running, Editing, Recording Macros
    run_macro_button = tk.Button(root, text="Run Macro")
    run_macro_button.grid(column=0, row=1, padx=(10, 10), pady=(10, 10))
    edit_macro_button = tk.Button(root, text="Edit Macro", command=edit_macro)
    edit_macro_button.grid(column=1, row=1, padx=(10, 10), pady=(10, 10))
    record_macro_button = tk.Button(root, text="Record Macro", command=record)
    record_macro_button.grid(column=2, row=1, padx=(10, 10), pady=(10, 10))
    end_record_macro_button = tk.Button(root, text="End Recording", command=end_record)
    end_record_macro_button.grid(column=3, row=1, padx=(10, 10), pady=(10, 10))
    # Dispays List of macros that you have recorded
    list_of_macros = os.listdir(str(Path(__file__).parent.resolve()) + "\macrolist")
    macro_list_box = tk.Listbox(root, height=15)
    macro_list_box.grid(
        column=0, row=2, padx=(10, 10), pady=(10, 10), columnspan=4, ipadx=120
    )
    for macro in list_of_macros:
        if macro[-4:] == ".txt":
            macro_list_box.insert("end", macro)
    # Macro Compiler Frame used to organize bottom half of main window in a separate grid
    root_frame = tk.LabelFrame(root)
    root_frame.grid(column=0, row=3, columnspan=4)
    root_frame.config(background="#252527", bd=0) # bd is border width = 0
    add_macro_list_button = tk.Button(root_frame, text="Add Macro")
    add_macro_list_button.grid(column=0, row=0, padx=(10, 10), pady=(10, 10))
    clear_macro_list_button = tk.Button(root_frame, text="Clear List")
    clear_macro_list_button.grid(column=1, row=0, padx=(10, 10), pady=(10, 10))
    run_macro_list_button = tk.Button(root_frame, text="Run Macro List 1-10x")
    run_macro_list_button.grid(column=2, row=0, padx=(10, 10), pady=(10, 10))
    repeat_combo_box = ttk.Combobox(root_frame, values = [1,2,3,4,5,6,7,8,9,10], width=3)
    repeat_combo_box.current(0)
    repeat_combo_box.grid(column=3, row=0, padx=(10, 10), pady=(10, 10))
    list_macros_run = []
    run_macro_list_box = tk.Listbox(root_frame, height=10)
    run_macro_list_box.grid(
        column=0, row=1, padx=(10, 10), pady=(10, 10), columnspan=4, ipadx=120
    )
    
    # Window that follows cursor, used to notify when recording and where the coordinates of the mouse are
    cursor_follow_window = tk.Tk()
    cursor_follow_window.overrideredirect(1)  # 0 shows bar 1 hides bar
    cursor_follow_window.geometry("140x20")
    coord_label = tk.Label(
        cursor_follow_window,
        text="Recording X: {0} Y: {1}".format(
            current_mouse_position_x, current_mouse_position_y
        ),
    ).grid(column=0, row=0)
    cursor_follow_window.withdraw()

    # Window used to obtain user input to modify an existing macro
    edit_window = tk.Tk()
    edit_window.title("Edit Macro")
    edit_window.geometry("300x350")
    edit_window.config(background="#252527")
    edit_window.resizable(width=False, height=False)
    description_one = tk.Label(
        edit_window,
        text="Pixel Disposition (0-20 pixel difference)",
        background="#252527",
        fg="white",
    )
    description_one.grid(column=0, row=0, padx=(10, 10), pady=(10, 0), sticky="w")
    macro_box_one = tk.Entry(edit_window)
    macro_box_one.grid(column=0, row=1, padx=(10, 10), pady=(5, 5), sticky="w")
    description_two_start = tk.Label(
        edit_window,
        text="Random Time Delay Per Press",
        background="#252527",
        fg="white",
    )
    description_two_start.grid(column=0, row=2, padx=(10, 10), pady=(10, 0), sticky="w")
    description_two_end = tk.Label(
        edit_window,
        text="Between Start-End Seconds, Range: 0-100 Seconds",
        background="#252527",
        fg="white",
    )
    description_two_end.grid(column=0, row=3, padx=(10, 10), pady=(0, 0), sticky="w")
    macro_box_two_start = tk.Entry(edit_window)
    macro_box_two_start.grid(column=0, row=4, padx=(10, 10), pady=(5, 5), sticky="w")
    macro_box_two_end = tk.Entry(edit_window)
    macro_box_two_end.grid(column=0, row=5, padx=(10, 10), pady=(5, 5), sticky="w")
    description_three = tk.Label(
        edit_window,
        text="Random Run Chance Percentage (0-100)",
        background="#252527",
        fg="white",
    )
    description_three.grid(column=0, row=6, padx=(10, 10), pady=(10, 0), sticky="w")
    macro_box_three = tk.Entry(edit_window)
    macro_box_three.grid(column=0, row=7, padx=(10, 10), pady=(5, 5), sticky="w")
    description_four = tk.Label(
        edit_window,
        text="Amount of times repeated (1-10)",
        background="#252527",
        fg="white",
    )
    description_four.grid(column=0, row=8, padx=(10, 10), pady=(10, 0), sticky="w")
    macro_box_four = tk.Entry(edit_window)
    macro_box_four.grid(column=0, row=9, padx=(10, 10), pady=(5, 5), sticky="w")
    submit_button = tk.Button(edit_window, text="Submit", command=edit_macro_submit)
    submit_button.grid(column=0, row=10, padx=(10, 10), pady=(20, 5), sticky="w")
    edit_window.withdraw()

    # Window used to ask user to name a text file the macro is saved to, after a macro is recorded
    input_window = tk.Tk()
    input_window.title("Name Macro")
    input_window.geometry("210x130")
    input_window.config(background="#252527")
    input_window.resizable(width=False, height=False)
    title1 = tk.Label(
        input_window,
        text="Name your macro \n(Only letters and numbers allowed)",
        background="#252527",
        fg="white",
    ).grid(column=0, row=0, padx=(10, 10), pady=(10, 10))
    inputbox = tk.Entry(input_window)  # Input box and submit button
    inputbox.grid(column=0, row=1, padx=(10, 10), pady=(5, 5))
    submit_button = tk.Button(input_window, text="Submit", command=export_macro)
    submit_button.grid(column=0, row=2, padx=(10, 10), pady=(5, 5))
    input_window.withdraw()

    root.protocol("WM_DELETE_WINDOW", on_closing_root)
    edit_window.protocol("WM_DELETE_WINDOW", on_closing_edit_window)
    input_window.protocol("WM_DELETE_WINDOW", on_closing_input_window)
    root.mainloop()
