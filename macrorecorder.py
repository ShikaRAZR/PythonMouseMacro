"""
Module - https://stackoverflow.com/questions/43183244/difference-between-module-and-class-in-python
https://www.pythonpool.com/python-class-vs-module/ 
Threads - https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread 
Mouse Record - https://pynput.readthedocs.io/en/latest/mouse.html#monitoring-the-mouse 

Will record, run, export import and modify mouse movements 
"""
from pynput import mouse
import pyautogui
from threading import Thread
from timeit import default_timer
import math
from pathlib import Path

# Global mouse listener variable
listener = None  # None is used to define a null value or no value
timer = None
recording = False
mouse_action_list = []
mouse_timer_list = []
mouse_coord_x_list = []
mouse_coord_y_list = []


def start_listener():  # started when program starts
    global listener
    print("Module - Before Listener Thread (Start)")
    with mouse.Listener(on_click=record_mouse_macro) as listener:
        listener.join()
    print("Module - After Listener Thread (Done)")


def end_listener():  # started when program ends
    global listener
    listener.stop()
    print("Module - Call To Stop Listener")


def record_mouse():
    global recording
    recording = True
    global timer
    timer = default_timer()
    global mouse_action_list
    global mouse_timer_list
    global mouse_coord_x_list
    global mouse_coord_y_list
    mouse_action_list = []
    mouse_timer_list = []
    mouse_coord_x_list = []
    mouse_coord_y_list = []
    print("Module - Record")


def stop_record_mouse():
    global recording
    recording = False
    global timer
    timer = None
    global mouse_action_list
    global mouse_timer_list
    global mouse_coord_x_list
    global mouse_coord_y_list
    del mouse_action_list[-2:]
    del mouse_timer_list[-2:]
    del mouse_coord_x_list[-2:]
    del mouse_coord_y_list[-2:]
    print("Module - End Record")


def record_mouse_macro(x, y, button, pressed):
    if recording:  # if recording save action/time/coordinates
        global timer
        global mouse_action_list
        global mouse_timer_list
        global mouse_coord_x_list
        global mouse_coord_y_list
        if pressed:
            print("Pressed")  # if pressed start a timer
            mouse_action_list.append("Pressed")  # saves action type to array
        else:
            print("Released")  # if released end the timer
            mouse_action_list.append("Released")  # saves action type to array
        time = round(default_timer() - timer, 4)
        timer = default_timer()
        print(time, " Seconds")
        print("Coord ", (x, y))
        print(" ")

        mouse_timer_list.append(time)  # saves time to array
        mouse_coord_x_list.append(x)  # saves x coord to array
        mouse_coord_y_list.append(y)  # saves y coord to array


def valid_macro_list():
    return len(mouse_action_list) > 0


def run_mouse_macro():
    print("Module - Run")


def export_mouse_macro(
    filename,
):  # starts when you stop recording, saves macro to a file
    path = Path(__file__).parent.resolve()
    fullfilepath = str(path) + "\macrolist\\" + filename + ".txt"
    print("TEST" + fullfilepath)
    f = open(fullfilepath, "w")
    f.write("0\n0\n0\n100\n1\n")
    for x in range(len(mouse_action_list)):
        f.write(mouse_action_list[x])
        f.write("\n")
        f.write(str(mouse_timer_list[x]))
        f.write("\n")
        f.write(str(mouse_coord_x_list[x]))
        f.write("\n")
        f.write(str(mouse_coord_y_list[x]))
        f.write("\n")
    print(mouse_action_list)
    print(mouse_timer_list)
    print(mouse_coord_x_list)
    print(mouse_coord_y_list)
    print("Module - Export")


def import_mouse_macro():
    print("Module - Import")


def modify_mouse_macro(fullfilepath, pixel_disposition_input, delay_start_input, delay_end_input, run_chance_input, repeat_input):
    with open(fullfilepath, "r") as file:
            data = file.readlines()
    data[0] = pixel_disposition_input+"\n"
    data[1] = delay_start_input+"\n"
    data[2] = delay_end_input+"\n"
    data[3] = run_chance_input+"\n"
    data[4] = repeat_input+"\n"
    with open(fullfilepath, "w") as file:
        file.writelines(data)
    print("Module - Modify")
