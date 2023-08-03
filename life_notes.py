"""
life_notes by Eliot Niedercorn

Version: 3.0 - Third Iteration
Last Updated: 29th July 2023

Description:
"life_notes" is a Python-based organization tool that provides a range of features, including daily notes management, calendar view, to-do lists, sticky notes, and password encryption. This minimalistic application offers a user-friendly graphical interface powered by the tkinter library.

Purpose:
The goal of "life_notes" is to help users effectively organize their daily tasks, manage notes, and stay productive. It is designed to be lightweight, open-source, and run directly on the user's computer offline.

Website: https://github.com/EliotNiedercorn/life_notes

License: GNU GENERAL PUBLIC LICENSE

Please refer to the README file for installation instructions and detailed usage information.

For contributions or feedback, feel free to get in touch with the project author: niedercorn.eliot@gmail.com

"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime
import os  # Allows to access files on the computer
import webbrowser
import re
from tkinter import filedialog


# File names
sticky_file = "sticky_note.txt"
todo_file = "todo.txt"

# Time Variables
day = datetime.datetime.today()  # Ex : 2022-08-09 12:34:37.829848
week = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
day_file = day.date().strftime("%d") + "_" + day.date().strftime("%m") + "_" + day.date().strftime("%y") + ".txt"  # Ex : 09_08_22.txt


############ Window Initialisation ############
window = tk.Tk()  # Create the window with the Tk Class
window.title("Life Notes")  # Window title

menu_bar = tk.Menu(window)
menu_bar.add_command(label="Save", command=lambda: save_all())
menu_bar.add_command(label="Password", command=lambda: password())
window.config(menu=menu_bar, bg="#FFFFE8")  # Background color and menu association


def center_window():
    # Function centering the window at the center of the screen
    app_width = 1200
    app_height = 700
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # Calculate position x and y coordinates
    x_coordinate = int((screen_width / 2) - (app_width / 2))
    y_coordinate = int((screen_height / 2) - (app_height / 2))
    window.geometry("{}x{}+{}+{}".format(app_width, app_height, x_coordinate, y_coordinate))  # Assign the dimension


center_window()

############ Main Widget Initialisation ############
window_frame = tk.Frame(window, bg="#FFFFE8")
window_frame.pack(fill="both", expand=True)  # je sais pas ce que ça fait mais c'est nécessaire comme le suivant
notebook = ttk.Notebook(window_frame)


############ Calendar Frame ############
calendar_frame = tk.Frame(notebook, bg="#FFFFE8")
notebook.add(calendar_frame, text="Calendar")

tododay_widget = tk.Text(calendar_frame, height=36, width=40, bg="#ACC8E6", padx=10, pady=5, relief="groove", wrap="word", undo=True, font=("Open Sans", 11))
sticky_note = tk.Text(calendar_frame, height=18, width=90, bg="#FFF7D1", padx=10, pady=5, relief="groove", wrap="word", undo=True, font=("Open Sans", 11))
todo = tk.Text(calendar_frame, height=16, width=90, bg="#D5896F", padx=10, pady=5, relief="groove", wrap="word", undo=True, font=("Open Sans", 11))

calendar_button = tk.Button(calendar_frame, text="", width=20, bg="#ADD8E6", font=("Open Sans", 10), command=lambda: open_calendar())
yesterday_button = tk.Button(calendar_frame, text="←", width=3, bg="#ADD8E6", relief="groove", font=("Open Sans", 10), command=lambda: change_day(day - datetime.timedelta(days=1)))
tomorrow_button = tk.Button(calendar_frame, text="→", width=3, bg="#ADD8E6", relief="groove", font=("Open Sans", 10), command=lambda: change_day(day + datetime.timedelta(days=1)))


############ Notes Frame ############
notes_frame = tk.Frame(notebook, bg="#FFFFE8")
notebook.add(notes_frame, text="Notes")
notes_text = tk.Text(notes_frame, height=18, width=90, bg="#FFF7D1", padx=10, pady=5, wrap="word", undo=True, font=("Open Sans", 11))
notes_text.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(notes_frame)  # Create a scrollbar for the listbox
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a listbox to display all notes
notes_listbox = tk.Listbox(notes_frame, height=5, width=20, selectmode=tk.SINGLE, bg="white", font=("Open Sans", 11))
notes_listbox.pack(side=tk.RIGHT, padx=(0, 20), pady=10, fill=tk.BOTH)


def create_file():
    # Get the input for the new file name using a file dialog
    new_file_name = filedialog.asksaveasfilename(initialdir="Notes/", title="Create New File", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if new_file_name:
        # Extract only the file name (without the path)
        new_file_name = os.path.basename(new_file_name)

        # Check if the file already exists
        if new_file_name in subjects:
            tk.messagebox.showerror("Error", "File already exists.")
            return

        # Create a new file in the folder
        with open(f"Notes/{new_file_name}", "w"):
            pass

        # Update the listbox with the new file name
        notes_listbox.insert(tk.END, re.sub(r'\.txt$', '', new_file_name))
        subjects.append(re.sub(r'\.txt$', '', new_file_name))


# Create the "Create File" button
create_file_button = tk.Button(notes_frame, text="+", command=create_file, bg="#FFFFE8", fg="black", font=("Open Sans", 8))
create_file_button.place(relx=0.983, rely=0.02, anchor=tk.NE)


scrollbar.config(command=notes_listbox.yview)  # Configure the scrollbar to work with the listbox


subjects = []
# Loop through all the files in the folder
for file in os.listdir("Notes/"):
    # Check if the file has a ".txt" extension
    if file.endswith('.txt'):
        # Remove the ".txt" extension and add to the list
        subjects.append(re.sub(r'\.txt$', '', file))  # Use regular expression to remove ".txt" extension if it exists


for subject in subjects:
    notes_listbox.insert(tk.END, subject)

previous_item = "Ideas"  # keep track of the previously selected item
index = subjects.index(previous_item)
notes_listbox.select_set(index)  # Set the default selection to the current subject
with open("Notes/Ideas.txt", "r") as open_file:
    notes_text.insert(tk.END, open_file.read())


def change_note(event):
    global previous_item
    selected_index = notes_listbox.curselection()
    if selected_index:  # Tout doit se faire dans ce if sinon lorsque je séléctionne none subject la fonction est déclenché
        # Save current note
        previous_file = "Notes/" + previous_item + ".txt"
        save_file(notes_text, previous_file)
        notes_text.delete("1.0", tk.END)

        # Get new note
        previous_item = notes_listbox.get(selected_index)
        file = "Notes/" + previous_item + ".txt"
        with open(file, "r") as open_file:
            notes = open_file.read()
        notes_text.insert(tk.END, notes)


notes_listbox.bind("<<ListboxSelect>>", change_note)  # Bind the listbox selection event to display_note method
notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


def widget_initialisation():
    tododay_widget.place(x=30, y=40)

    sticky_note.place(x=420, y=40)
    with open(sticky_file, "r") as open_sticky_file:  # When you use with statement with open function, you do not need to close the file at the end, because with would automatically close it for you.
        sticky_note.insert(tk.INSERT, open_sticky_file.read())

    todo.place(x=420, y=380)
    with open(todo_file, "r") as open_todo_file:
        todo.insert(tk.INSERT, open_todo_file.read())

    calendar_button.place(x=115, y=8)
    yesterday_button.place(x=70, y=8)
    tomorrow_button.place(x=300, y=8)


widget_initialisation()


############ Time Gestion ############
def day_init(day_input, file_name):
    # Write the content of a day file in day_text, if the file does not exist create a new one
    day_text = week[day_input.weekday()] + " " + day_input.date().strftime("%d/%m/%y")  # Texte au dessus de tododay # Ex : Mardi 09/08/22
    calendar_button["text"] = day_text
    try:
        with open(file_name, 'r') as open_file:
            for line in open_file:
                tododay_widget.insert(tk.INSERT, line)
    except OSError:  # Create a new file if it does not exist
        with open(file_name, "w"):
            pass


day_init(day_input=day, file_name=day_file)


def change_day(new_day):
    global day  # Permet d'identifier la variable day comme la variable global et pas comme une variable locale dans la fonction
    global day_file
    save_day()  # Save the text before changing day
    tododay_widget.delete(1.0, tk.END)
    day = new_day
    day_file = day.date().strftime("%d") + "_" + day.date().strftime("%m") + "_" + day.date().strftime("%y") + ".txt"
    day_init(day, day_file)
    return


def open_calendar():
    calendar_window = tk.Toplevel(window)
    calendar_window.geometry("251x225")
    calendar_widget = Calendar(calendar_window, selectmode='day', day=day.day, month=day.month, year=day.year)
    calendar_widget.place(x=0, y=0)
    calendar_widget.pack(pady=5, padx=5)
    change_date_button = tk.Button(calendar_window, text="Change Date", bg="lightgrey", width=33, command=lambda: calendar_submit(calendar_window, calendar_widget.get_date()))
    change_date_button.place(x=5, y=195)
    return


def calendar_submit(calendar_window, new_date):
    new_date = datetime.datetime.strptime(new_date, '%m/%d/%y')
    change_day(new_date)
    calendar_window.destroy()
    return


############ Save Functions ############
def save_file(text_widget, file_name):
    # Function that save the text widget's text in a file
    text = text_widget.get(1.0, 'end-1c')  # Get the text in the text field
    with open(file_name, "w") as w_file:  # Open the save file for writing
        w_file.write(text)
    return


def save_day():
    text = tododay_widget.get(1.0, 'end-1c')
    with open(day_file, 'w') as w_day_file:
        w_day_file.write(text)
    return


def save_all():
    save_day()
    save_file(sticky_note, sticky_file)
    save_file(todo, todo_file)
    return


############ Password Gestion ############
def password():
    password_window = tk.Toplevel(window)
    password_window.geometry("250x150")

    p_var = tk.StringVar()
    p_entry = tk.Entry(password_window, textvariable=p_var)
    p_entry.place(x=75, y=10)

    key_var = tk.StringVar()
    key_entry = tk.Entry(password_window, textvariable=key_var, show="*")
    key_entry.place(x=75, y=40)

    p_label = tk.Label(password_window, text="Password :")
    p_label.place(x=10, y=10)

    key_label = tk.Label(password_window, text="Key :")
    key_label.place(x=30, y=40)

    submit_button = tk.Button(password_window, text="Submit", width=5,
                              command=lambda: submit_password(password_window, key_var, p_var))
    submit_button.place(x=110, y=80)

    os.startfile("password.txt")
    return


def submit_password(password_window, key_input, p_input):
    key = key_input.get()
    p = p_input.get()

    characters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                  "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                  "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    p_lenght = len(p)
    key_lenght = len(key)
    res = ""

    for i in range(p_lenght):

        characters_order = characters.index(p[i].lower())  # Returns the index of the specified element in the list
        new_value = i * characters_order
        if i < key_lenght:
            new_value = new_value + characters.index(key[i].lower())  # Takes in account the password
        while new_value > 35:
            new_value = new_value // 2  # Assure that we stay in the characters list range
        get_uppercase = p[i].isupper()  # Keep track if the character is uppercase
        if get_uppercase:
            res = res + characters[new_value].upper()
        else:
            res = res + characters[new_value]

    window.clipboard_append(res)
    password_window.destroy()
    return res


############ Closing ####################
def on_closing():
    # Function that save the text when the window is closed
    save_day()
    save_file(sticky_note, sticky_file)
    save_file(todo, todo_file)
    save_file(notes_text, "Notes/" + previous_item + ".txt")
    window.destroy()  # Close the window


window.protocol("WM_DELETE_WINDOW", on_closing)  # Run on_closing() when the window is closed
tk.mainloop()  # Show the window
