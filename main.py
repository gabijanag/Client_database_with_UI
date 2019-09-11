from tkinter import *
import sqlite3


conn = sqlite3.connect("clients.db")
c = conn.cursor()

mainWindow = Tk()
mainWindow.title("Clients database")
mainWindow.iconbitmap(r'team2.ico')
top = Frame(mainWindow)
middle = Frame(mainWindow)
bottom = Frame(mainWindow)
entries = []  # empty list for future entries
editingExisting = ""  # empty string when entry is not entered


class Client:
    def __init__(self, name, lastName, age):
        self.name = name
        self.lastName = lastName
        self.age = age


def create_table():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS clients (
                Name text,
                Last_Name text,
                Age integer
                )""")


# Get all entries and show them in a Listbox
def get_list():
    global entries
    entries = []
    c.execute("SELECT * FROM clients")
    for client in c.fetchall():
        entries.append(client)


# Refresh all entries listbox and clear entry boxes
def clear_entry_boxes():
    allEntriesBox.delete(0, END)  # refreshes list
    allEntriesBox.insert(END, *entries)
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')
    entry3.delete(0, 'end')
    entry1.focus() # sets cursor at namebox


def add_entry(event):
    global editingExisting
    if not editingExisting:  # If a new entry is entered
        client = Client(entry1.get(), entry2.get(), entry3.get()) # take the entries
        with conn:  # put them into people database
            c.execute(f"INSERT INTO client VALUES('{client.name}', \
'{client.lastName}', {client.age})")
    else:
        with conn:  # otherwise update the data with current entry information
            c.execute(f"UPDATE clients SET Name = '{entry1.get()}',\
             Last_Name = '{entry2.get()}', Age = {entry3.get()}\
              WHERE Name = '{editingExisting.name}' AND Last_Name = '{editingExisting.lastName}'")
            editingExisting = ""
    get_list()  # show the new list
    clear_entry_boxes()  # clear entry boxes


def delete():
    global entries
    global editingExisting
    active = entries[allEntriesBox.curselection()[0]]  # Select the entry where the cursor is
    client = Client(active[0], active[1], active[2])  # take all three columns of that entry
    entries.remove(active)  # remove selected entry from the list box
    with conn:  # remove selected entry from the database
        c.execute(f"DELETE from clients WHERE Name = '{client.name}' \
        AND Last_Name = '{client.lastName}'")
    editingExisting = ""  # clear editing existing string
    clear_entry_boxes()  # clear entry boxes


def edit():
    global entries
    global editingExisting
    active = entries[allEntriesBox.curselection()[0]]  # Select the entry where the cursor is
    client = Client(active[0], active[1], active[2])  # take all three columns of that entry
    editingExisting = client
    clear_entry_boxes()
    entry1.insert(0, client.name)
    entry2.insert(0, client.lastName)
    entry3.insert(0, client.age)


# UI
newLineTitle = Label(top, text="Enter Client", width = 40)
name = Label(top, text="Name")
entry1 = Entry(top)
lastName = Label(top, text="Last Name")
entry2 = Entry(top)
age = Label(top, text="Age")
entry3 = Entry(top)
entryButton = Button(top, text="Enter")
entryButton.bind("<Button-1>", add_entry)
entry1.bind("<Return>", add_entry)
entry2.bind("<Return>", add_entry)
entry3.bind("<Return>", add_entry)
allEntriesBox = Listbox(middle, selectmode=SINGLE, width=40, height=20)
editButton = Button(bottom, text="Edit", command=edit)
deleteButton = Button(bottom, text="Delete", command=delete)

create_table()
get_list()
allEntriesBox.insert(END, *entries)

# UI defining positions
newLineTitle.grid(row=0, columnspan=2)
name.grid(row=1, column=0)
entry1.grid(row=1, column=1)
lastName.grid(row=2, column=0)
entry2.grid(row=2, column=1)
age.grid(row=3, column=0)
entry3.grid(row=3, column=1)
entryButton.grid(row=4, columnspan=2)
allEntriesBox.grid(row=0, sticky=W+E)
editButton.pack()
deleteButton.pack()
top.pack()
middle.pack()
bottom.pack()

mainWindow.mainloop()
