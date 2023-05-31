from tkinter import *
from tkcalendar import DateEntry

root = Tk()
root.geometry('600x400')

cal = DateEntry(root, selectmode='day')
cal.pack(pady=20)

def grab_date():
    my_label.config(text=cal.get_date())

my_button = Button(root, text='Get Date', command=grab_date)
my_button.pack(pady=20)

my_label = Label(root, text='')
my_label.pack(pady=20)

root.mainloop()
