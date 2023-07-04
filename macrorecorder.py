"""
Module - https://stackoverflow.com/questions/43183244/difference-between-module-and-class-in-python
https://www.pythonpool.com/python-class-vs-module/ 
Threads - https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread 
Mouse Record - https://pynput.readthedocs.io/en/latest/mouse.html#monitoring-the-mouse 

Will record, run, export import and modify mouse movements 
"""
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
from timeit import default_timer
from pathlib import Path
import random
import numpy as np
import time

# Variables for mouse movement generation
sqrt3 = np.sqrt(3)
sqrt5 = np.sqrt(5)

# Variables for recording mouse actions
listener = None  # Global mouse listener variable
timer = None
recording = False
mouse_action_list = []
mouse_timer_list = []
mouse_coord_x_list = []
mouse_coord_y_list = []
stop_macro_running = True
mouse_controller = Controller()

def start_mouse_listener():  # started when program starts
    global mouse_listener
    print("Module - Before Mouse Listener Thread (Start)")
    with mouse.Listener(on_click=record_mouse_macro) as mouse_listener:
        mouse_listener.join()
    print("Module - After Mouse Listener Thread (Done)")
    

def end_mouse_listener():  # started when program ends
    global mouse_listener
    mouse_listener.stop()
    print("Module - Call To Stop Mouse Listener")

def start_keyboard_listener():
    global keyboard_listener
    print("Module - Before Keyboard Listener Thread (Start)")
    with keyboard.Listener(on_press=on_press) as keyboard_listener:
        keyboard_listener.join()
    print("Module - After Keyboard Listener Thread (Done)")

def end_keyboard_listener():
    global keyboard_listener
    keyboard_listener.stop()
    print("Module - Call To Stop Keyboard Listener")

def on_press(key):
    if key == keyboard.Key.esc:
        global stop_macro_running
        stop_macro_running=True

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


def valid_macro(fullfilepath):
    if Path(fullfilepath).is_file():
        with open(fullfilepath, "r") as file:
                data = file.readlines()
        if(int(data[0])>=0 and int(data[0])<=20 
           and int(data[1])>=0 and int(data[1])<=100 
           and int(data[2])>=0 and int(data[2])<=100
           and int(data[2]) - int(data[1])>=0
           and int(data[3])>=0 and int(data[3])<=100
           and int(data[4])>=0 and int(data[4])<=10):
            print("Module - Valid Macro True")
            return True
    print("Module - Valid Macro False")
    return False

 
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


def run_mouse_macro(fullfilepath): # sets up a list of coordinates based on file (fullfilepath) to move mouse
    if valid_macro(fullfilepath):
        global stop_macro_running
        stop_macro_running=False
        with open(fullfilepath, "r") as file:
            data = file.readlines()
        global mouse_action_list
        global mouse_timer_list
        global mouse_coord_x_list
        global mouse_coord_y_list
        mouse_action_list = []
        mouse_timer_list = []
        mouse_coord_x_list = []
        mouse_coord_y_list = []
        # Macro Modifiers
        pixel_disposition_input = int(data[0])
        delay_start_input = int(data[1])
        delay_end_input = int(data[2])
        run_chance_input = int(data[3])
        repeat_input = int(data[4])
        print(pixel_disposition_input)
        print(delay_start_input)
        print(delay_end_input)
        print(run_chance_input)
        print(repeat_input)
        # Modifying Macro
        for x in range(5, len(data),4):
            mouse_action_list.append(data[x].strip())
            delay = 0
            dispostion_x = 0
            dispostion_y = 0
            if(delay_end_input-delay_start_input>0 and data[x].strip() == "Pressed"):
                delay = random.randint(delay_start_input, delay_end_input)
            if(pixel_disposition_input>0):
                dispostion_x = random.randint(-1*pixel_disposition_input, pixel_disposition_input)
                dispostion_y = random.randint(-1*pixel_disposition_input, pixel_disposition_input)
            
            mouse_timer_list.append(float(data[x+1])+delay)
            mouse_coord_x_list.append(int(data[x+2])+dispostion_x)
            mouse_coord_y_list.append(int(data[x+3])+dispostion_y)
        print(mouse_action_list)
        print(mouse_timer_list)
        print(mouse_coord_x_list)
        print(mouse_coord_y_list)
        # Running Macro
        for x in range(repeat_input):
            if stop_macro_running:
                return False
            if(random.randint(1,100)<=run_chance_input):
                for x in range(0,len(mouse_action_list),2):
                    if stop_macro_running:
                        return False
                    time.sleep(mouse_timer_list[x])
                    start_x_coord = mouse_coord_x_list[x]
                    start_y_coord = mouse_coord_y_list[x]
                    end_x_coord = mouse_coord_x_list[x+1]
                    end_y_coord = mouse_coord_y_list[x+1]
                    points = [[start_x_coord,start_y_coord]]
                    wind_mouse(start_x_coord,start_y_coord,end_x_coord,end_y_coord,move_mouse=lambda x,y: points.append([x,y]))
                    points.append([end_x_coord,end_y_coord])
                    time_interval = round((mouse_timer_list[x+1]/len(points)), 5)
                    drag_mouse(points, time_interval) # moving mouse
                    for point in points:
                        print(point)
                    print(time_interval)
    print("Module - Run")

def drag_mouse(points, time_interval): # takes an array of coordinates (points) and drags on an interval (time_interval)
    mouse_controller.position = (points[0][0],points[0][1])
    mouse_controller.press(Button.left)
    for x in range(1, len(points)):
        if stop_macro_running:
                mouse_controller.release(Button.left)
                return False
        time.sleep(time_interval)
        mouse_controller.move(points[x][0]-points[x-1][0], points[x][1]-points[x-1][1])
    mouse_controller.release(Button.left)
    print("Module - Move")

def wind_mouse(start_x, start_y, dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=lambda x,y: None):
    '''
    https://ben.land/post/2021/04/25/windmouse-human-mouse-movement/
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational fornce
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    '''
    current_x,current_y = start_x,start_y
    v_x = v_y = W_x = W_y = 0
    while (dist:=np.hypot(dest_x-start_x,dest_y-start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
            W_y = W_y/sqrt3 + (2*np.random.random()-1)*W_mag/sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random()*3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0*(dest_x-start_x)/dist
        v_y += W_y + G_0*(dest_y-start_y)/dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0/2 + np.random.random()*M_0/2
            v_x = (v_x/v_mag) * v_clip
            v_y = (v_y/v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))
        if current_x != move_x or current_y != move_y:
            #This should wait for the mouse polling interval
            move_mouse(current_x:=move_x,current_y:=move_y)
    return current_x,current_y

