from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

def new_list():
    # Set the root window title.
    root.title("New list")

    for i in range(incomplete_box.size()):
        incomplete_box.delete(0)

    for i in range(complete_box.size()):
        complete_box.delete(0)

# Open a to-do list text file. The first line of the file contains an integer 
# that denotes the number of incomplete items in the list, which is used to 
# create two separate lists for incomplete items and complete items.
def open_file():
    file_name = filedialog.askopenfilename(title = "Select a file",
                                           filetypes = (("Text files",
                                                         "*.txt*"),
                                                        ("All files",
                                                         "*.*"))) 

    try:
        f = open(file_name)
        text = f.readlines()
        num_inc = int(text[0].strip())
        incomplete = text[1:num_inc + 1]
        complete = text[num_inc + 1:]
        f.close()
        insert_lists(incomplete, complete)
        # Set the root window title.
        root.title(file_name)
    except:
        pass

def write_file():
    file_name = filedialog.asksaveasfilename(title = "Select a file",
                                             filetypes = (("Text files",
                                                           "*.txt*"),
                                                          ("All files",
                                                           "*.*")))

    if ".txt" not in file_name:
        file_name += ".txt"

    try:
        f = open(file_name, "w")
        f.write(str(incomplete_box.size()) + '\n')
        for i in range(incomplete_box.size()):
            f.write(incomplete_box.get(i))
        for i in range(complete_box.size()):
            f.write(complete_box.get(i))
        root.title(file_name)
        f.close()
    except:
        pass

# Insert each item from a file into its respective box.
def insert_lists(incomplete, complete):
    for i in range(len(incomplete)):
        incomplete_box.insert(i, incomplete[i])

    for i in range(len(complete)):
        complete_box.insert(i, complete[i])

# Add an item to the incomplete box.
def add_incomplete_item():
    item = simpledialog.askstring("Input", "Enter a new item",
                                  parent = root)
    item += '\n'
    incomplete_box.insert(END, item)

def edit_item():
    # Determine the selected item an item box.
    incomplete_selected = incomplete_box.curselection()
    complete_selected = complete_box.curselection()
    if len(incomplete_selected) > 0:
        box = incomplete_box
        item = incomplete_selected[0]
    elif len(complete_selected) > 0:
        box = complete_box
        item = complete_selected[0]
    else:
        messagebox.showerror("Error", "No item selected.")
        return
   
    # Get and apply the edit.
    new_item = simpledialog.askstring("Input", "Enter the edited item",
                                      parent = root)
    new_item += '\n'
    box.delete(item)
    box.insert(item, new_item)

def remove_item():
    # Determine the selected item an item box.
    incomplete_selected = incomplete_box.curselection()
    complete_selected = complete_box.curselection()
    if len(incomplete_selected) > 0:
        box = incomplete_box
        item = incomplete_selected[0]
    elif len(complete_selected) > 0:
        box = complete_box
        item = complete_selected[0]
    else:
        messagebox.showerror("Error", "No item selected.")
        return

    box.delete(item)

def mark_complete():
    incomplete_selected = incomplete_box.curselection()

    if len(incomplete_selected) == 0:
        messagebox.showerror("Error", "No item selected in the incomplete box.")
        return
    
    complete_box.insert(END, incomplete_box.get(incomplete_selected))
    incomplete_box.delete(incomplete_selected)

def mark_incomplete():
    complete_selected = complete_box.curselection()

    if len(complete_selected) == 0:
        messagebox.showerror("Error", "No item selected in the complete box.")

    incomplete_box.insert(END, complete_box.get(complete_selected))
    complete_box.delete(complete_selected)

root = Tk()
frame = ttk.Frame(root, padding = 10)

# Create menu bar.
menubar = Menu(root)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label = "New", command = new_list)
filemenu.add_command(label = "Open", command = open_file)
filemenu.add_command(label = "Save", command = write_file)
menubar.add_cascade(label = "File", menu = filemenu)
root.config(menu = menubar)

# Instantiate a grid.
frame.grid()

# Create labels for the item boxes.
ttk.Label(frame, text = "Incomplete").grid(column = 0, row = 0, 
                                             columnspan = 2)
ttk.Label(frame, text = "Complete").grid(column = 3, row = 0, 
                                             columnspan = 2)

# Create item boxes.
incomplete_box = Listbox(frame)
complete_box = Listbox(frame)
incomplete_box.grid(column = 0, row = 1, columnspan = 2)
complete_box.grid(column = 3, row = 1, columnspan = 2)

# Create buttons.
ttk.Button(frame, text = "Mark Complete",
           command = mark_complete).grid(column = 0, row = 2)
ttk.Button(frame, text = "Mark Incomplete",
           command = mark_incomplete).grid(column = 1, row = 2)
ttk.Button(frame, text = "Add Item",
           command = add_incomplete_item).grid(column = 2, row = 2)
ttk.Button(frame, text = "Edit Item",
           command = edit_item).grid(column = 3, row = 2)
ttk.Button(frame, text = "Remove Item",
           command = remove_item).grid(column = 4, row = 2)

# Start the main loop.
root.mainloop()
