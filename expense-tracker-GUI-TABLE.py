from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import sqlite3

# create root window
root = Tk()
root.title("Tkinter-Expense-Tracker")
root.geometry("800x800")
root.resizable(0,0)
root['background'] = '#6A287E'



# connect to database
connector = sqlite3.connect('expense_tracker.db')

# create a cursor
cursor = connector.cursor()

# create a table
cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                date text,
                amount float,
                name text,
                mode text)""")


def list_all_expenses(table):
    # connect to database
    connector = sqlite3.connect('expense_tracker.db')

    # create a cursor
    cursor = connector.cursor()

    # clear current data
    table.delete(*table.get_children())
    
    # retreive date
    all_data = cursor.execute("SELECT * FROM expenses")

    data = all_data.fetchall()

    # populate date to treeview
    for values in data:
        table.insert('', END, values=values)
    

    #COMMIT CHANGES
    connector.commit()

    #CLOSE CONNECTION
    connector.close()

def submit():
    global table
    
    # connect to database
    connector = sqlite3.connect('expense_tracker.db')

    # create a cursor
    cursor = connector.cursor()

    if not date.get() or not amount.get() or not name.get() or not mode.get():
        mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button.")

    else:
        # insert values into table
        cursor.execute("INSERT INTO expenses (date, amount, name, mode) VALUES (?, ?, ?, ?)",
                       (str(date.get()),float(amount.get()),str(name.get()),str(mode.get())))
    
        #COMMIT CHANGES
        connector.commit()

        #CLOSE CONNECTION
        connector.close()

        list_all_expenses(table)
        clear_fields()


def delete_expense():
    global table

    # connect to database
    connector = sqlite3.connect('expense_tracker.db')

    # create a cursor
    cursor = connector.cursor()

    if not table.selection():
        mb.showerror('No record selected!', 'Please select a record to delete!')
        return


    current_selected_expense = table.item(table.focus())
    values_selected = current_selected_expense['values']

    surety = mb.askyesno('Are you sure?', f'Are you sure that you want tp delete the expense ID: {values_selected[0]}')

    if surety:
        connector.execute('DELETE FROM expenses WHERE ID=%d' %values_selected[0])

        #COMMIT CHANGES
        connector.commit()

        #CLOSE CONNECTION
        connector.close()

        list_all_expenses(table)

        mb.showinfo('Expense deleted successfully!', 'The expense you wanted to delete has been removed sucessfully!')
    

def clear_fields():
    date.delete(0,END)
    amount.delete(0,END)
    name.delete(0,END)
    mode.delete(0,END)

# tree frame
tree_frame = Frame(root)
# tree frame placement
tree_frame.place(relx=.15,rely=.4,relwidth=.70,height=300)

# table widget
table = ttk.Treeview(tree_frame, columns=('ID',
                                          'Date',
                                          'Amount',
                                          'Name',
                                          'Mode'))
# table headings
table.heading('ID',text='ID No.', anchor = CENTER)
table.heading('Date',text='Date', anchor = CENTER)
table.heading('Amount',text='Amount', anchor = CENTER)
table.heading('Name',text='Name', anchor = CENTER)
table.heading('Mode',text='Mode', anchor = CENTER)

# table columns
table.column('#0', width=0, stretch=NO)
table.column('#1', width=60, stretch=NO)
table.column('#2', width=108, stretch=NO)
table.column('#3', width=140, stretch=NO)
table.column('#4', width=150, stretch=NO)
table.column('#5', width=100,stretch=NO)

# table placement
table.place(relx=0,y=0, height=300, relwidth=1)

# entry frame
entry_frame = Frame(root,  bg='#c0c2c9')

# entry frame placement
entry_frame.place(relx=.05,rely=.1,relwidth=.90,relheight=.30)

# entry frame labels
date_label = Label(entry_frame, text='Date', bg='#c0c2c9')
date_label.place(relx=.05,rely=.1)
amount_label = Label(entry_frame, text='Amount', bg='#c0c2c9')
amount_label.place(relx=.05,rely=.3)
name_label = Label(entry_frame, text='Name', bg='#c0c2c9')
name_label.place(relx=.5,rely=.1)
mode_label = Label(entry_frame, text='Mode', bg='#c0c2c9')
mode_label.place(relx=.5,rely=.3)
main_label = Label(root, text='Expense Tracker', bg='#6A287E', fg='white', font=('Arial', 25))
main_label.place(relx=.35,rely=.04)

# entry frame boxes
date = Entry(entry_frame, width=30)
date.place(relx=.05,rely=.2)
amount = Entry(entry_frame, width=30)
amount.place(relx=.05,rely=.4)
name = Entry(entry_frame, width=30)
name.place(relx=.5, rely=.2)
mode = Entry(entry_frame, width=30)
mode.place(relx=.5, rely=.4)

# entry frame buttons
submit_button = Button(entry_frame, text='Add Expense', width=20, command=submit, bg='#6A287E', fg='white')
submit_button.place(relx=.05, rely=.6)
clear_fields_button = Button(entry_frame, text='Clear Entry Fields', width=20, command=clear_fields, bg='#6A287E', fg='white')
clear_fields_button.place(relx=.05, rely=.75)
delete_expense_button = Button(entry_frame, text='Remove Expense', width=20, command=delete_expense, bg='#6A287E', fg='white')
delete_expense_button.place(relx=.5, rely=.6)

# commit changes
connector.commit()

#close connection
connector.close()

list_all_expenses(table)
root.update()
root.mainloop()
