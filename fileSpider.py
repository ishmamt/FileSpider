# ~~ made by sed_cat ~~

# This script creates a basic GUI

# imports
import tkinter as tk
from tkinter import filedialog, Text
from PIL import Image, ImageTk
from tkinter import font
from filecopy import copyfile
from filecopy import createdir
from login import user_verify


# some important constants
WIDTH = 800
HEIGHT = 500
destination = ''
target = ''
myfont = ('Microsoft YaHei Light', '12')  # font face and size
buttonfont = ('Microsoft YaHei Light', '10')
verified = False  # toggle for giving access to the user after verification


def destSelection(dest_frame):
    # function to open the file browser and showing selected dir
    global destination
    destination = filedialog.askdirectory(initialdir="/", title='Select folder')
    dest_dir = tk.Label(dest_frame, text=destination, bg='#172736', fg='white', font=myfont, justify='left')
    dest_dir.place(relx=0, rely=0.4, relheight=0.3, relwidth=1)


def targetSelection(targ_frame):
    # function to open the file browser and showing selected dir
    global target
    target = filedialog.askdirectory(initialdir="/", title='Select folder')
    targ_dir = tk.Label(targ_frame, text=target, bg='#172736', fg='white', font=myfont, justify='left')
    targ_dir.place(relx=0, rely=0.4, relheight=0.3, relwidth=1)


def start_copy(terminal_frame):
    global destination
    global target
    # check if the user has selected both the destination and target folder
    if len(destination) > 1 and len(target) > 1:
        # actual copying command
        createdir(target, destination)
        count = copyfile(target, destination)

        # confirmation
        done_text = tk.Label(terminal_frame, bg='#172736', fg='white', text='Done !', font=myfont)
        done_text.place(relx=0.5, rely=0.35, anchor='n')
        count_text = tk.Label(terminal_frame, bg='#172736', fg='white', text=f'Successfully copied {count} files', font=myfont)
        count_text.place(relx=0.5, rely=0.45, anchor='n')


def terminalGUI():
    # creates the terminal that holds the copy button and the confirmation prompt
    copy_frame = tk.Frame(root, bg='#172736')
    copy_frame.place(relx=0.5, rely=0.37, relheight=0.1, relwidth=0.35, anchor='n')

    startcopy = tk.Button(copy_frame, text='Start Copying', font=buttonfont, command=lambda: start_copy(terminal_frame))
    startcopy.place(relwidth=1, relheight=1, relx=0, rely=0)

    # adding the frame for the terminal
    terminal_frame = tk.Frame(root, bg='#172736')
    terminal_frame.place(relx=0.1, rely=0.5, relheight=0.45, relwidth=0.8)


def copyGUI():
    # this function will create the frames for folder selection

    # adding button to select destination folder
    dest_frame = tk.Frame(root, bg='#172736')
    dest_frame.place(relx=0.1, rely=0.03, relheight=0.15, relwidth=0.8)

    dest_text = tk.Label(dest_frame, bg='#172736', fg='white', text='Select destination folder', font=myfont)
    dest_text.place(relx=0, rely=0.1, relheight=0.33, relwidth=0.3)

    dest_button = tk.Button(dest_frame, text='Select', font=buttonfont, command=lambda: destSelection(dest_frame))
    dest_button.place(relx=0.83, rely=0.1, relheight=0.3, relwidth=0.15)

    # adding button to select files to copy
    targ_frame = tk.Frame(root, bg='#172736')
    targ_frame.place(relx=0.1, rely=0.2, relheight=0.15, relwidth=0.8)

    targ_text = tk.Label(targ_frame, bg='#172736', fg='white', text='Select folder to copy', font=myfont)
    targ_text.place(relx=-0.02, rely=0.1, relheight=0.33, relwidth=0.3)

    targ_button = tk.Button(targ_frame, text='Select', font=buttonfont, command=lambda: targetSelection(targ_frame))
    targ_button.place(relx=0.83, rely=0.1, relheight=0.3, relwidth=0.15)


def pass_button(usr_pass):
    global verified
    # check to see if user has entered something
    if len(usr_pass) > 0:
        verified = user_verify(usr_pass)
        GUI()  # this will create the GUI for later parts (duh...)


def loginGUI():
    # this function creates the GUI elements for login prompt

    # adding bg gradient image
    login_bg = tk.Label(root, image=bgGradient)
    login_bg.place(relheight=1, relwidth=1)

    # adding frame for the login prompt
    login_frame = tk.Frame(root, bg='#172736')
    login_frame.place(relwidth=0.9, relheight=0.75, relx=0.05, rely=0.1)

    # setting up login text prompt
    login_text = tk.Label(login_frame, bg='#172736', fg='white', text='Enter Password for database: ', font=myfont)
    login_text.place(relx=0.1, rely=0.2)

    # setting up field for entering password
    login_pass = tk.Entry(login_frame, font=myfont)
    login_pass.place(relx=0.43, rely=0.18, relheight=0.1, relwidth=0.5)

    # setting up the button to submit password
    login_button = tk.Button(login_frame, text='Submit', font=buttonfont, command=lambda: pass_button(login_pass.get()))
    login_button.place(relx=0.45, rely=0.3, relheight=0.08, relwidth=0.1)

    # helpful note for users
    login_help = tk.Label(login_frame, bg='#172736', fg='white', text='If database is not yet set, it will save as new password.', font=myfont)
    login_help.place(relx=0.25, rely=0.75)


def GUI():
    if verified:
        # adding bg gradient image
        gui_bg = tk.Label(root, image=bgGradient)
        gui_bg.place(relwidth=1, relheight=1)
        copyGUI()
        terminalGUI()


# .......the main GUI loop starts here.......


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# whatever is written between this is gonna be in the gui

root = tk.Tk()  # creating a root as the main body of the GUI
bgGradient = tk.PhotoImage(file='bgGradient.jpg')  # background image

# canvas to hold the shape of GUI by drawing a rectangle
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)

# this calls all the gui functions
loginGUI()

canvas.pack()

root.mainloop()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
