#!/usr/bin/env python
#dvjTagManager.py - main program for the daVinciJrTagManager set up programs
#Copyright (C) 2017  Mark Ferrick
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at my option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


from tkinter import *
from myFunctions import *
from SQLbackend import *

#Create the window object    # All windows object between window=Tk() and window.mainloop()
window=Tk()
#window.geometry("650x400")
window.title("DaVinci Tag Generator")

temperature=IntVar()
spoolsize=IntVar()
sStatus=StringVar()
flipper = BooleanVar()

# Menu System
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Create or Update Database", command=lambda: dbCreateUpdate(sStatus, window, tkFileDialog))

filemenu.add_separator()

filemenu.add_command(label="Exit", command=lambda: myExit(window))

menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=lambda: myHelp())
helpmenu.add_command(label="About...", command=lambda: myHelpAbout())
menubar.add_cascade(label="Help", menu=helpmenu)

window.config(menu=menubar)

# define labels
l1=Label(window, text="id")
l1.grid(row=1, column=5, sticky=E)

l2=Label(window, text="UID-1")
l2.grid(row=2, column=5, sticky=E)

l3=Label(window, text="UID-2")
l3.grid(row=3, column=5, sticky=E)

l4=Label(window, text="Password")
l4.grid(row=4, column=5, sticky=E)

l5=Label(window, text="PACK")
l5.grid(row=5, column=5, sticky=E)

lUsed=Label(window, text="Used")
lUsed.grid(row=6, column=5, sticky=E)

l6=Label(window, text="Page 9 Data")
l6.grid(row=7, column=5, sticky=E)

lSearchResults=Label(window, text="Search Results")
lSearchResults.grid(row=9, column=0)

sStatus.set('Status:')
lStatus=Label(window, textvariable=sStatus)
lStatus.grid(row=21, column=0, columnspan=3, sticky=W)

# define entries
id_text=IntVar()
e1=Entry(window, textvariable=id_text)
id_text.set("")
e1.grid(row=1, column=6)

UID1_text=StringVar()
e2=Entry(window, textvariable=UID1_text)
e2.grid(row=2, column=6)

UID2_text=StringVar()
e3=Entry(window, textvariable=UID2_text)
e3.grid(row=3, column=6)

password_text=StringVar()
e4=Entry(window, textvariable=password_text)
e4.grid(row=4, column=6)

pack_text=StringVar()
e5=Entry(window, textvariable=pack_text)
e5.grid(row=5, column=6)

used_text=StringVar()
e6=Entry(window, textvariable=used_text)
e6.grid(row=6, column=6)

page9_text=StringVar()
e7=Entry(window, textvariable=page9_text)
e7.grid(row=7, column=6)


# define ListBox and scroll bar
list1=Listbox(window, height=10, width=40)
list1.grid(row=10, column=0, rowspan=10, columnspan=2)
list1.bind('<<ListboxSelect>>', lambda event: onselect(event, id_text, UID1_text, UID2_text, password_text, pack_text, used_text ))

sb1=Scrollbar(window)
sb1.grid(row=10, column=2, rowspan=10, sticky=W, ipady = 60)
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

flipper_check = Checkbutton(window, text="Save in Flipper Zero format.", variable=flipper)
flipper_check.grid(row=0, column=1)

def save_tag(status, id, uid1, uid2, pword, pack, temperature, spoolsize, page9, flipper):
    useUID(sStatus, id)
    generateTagData(status, uid1, uid2, pword, pack, temperature, spoolsize, page9, flipper)

b7=Button(window, text="Save NFC Tag Data", bg='green', width=16, state=DISABLED, command=lambda: save_tag(sStatus, int(e1.get()), e2.get(), e3.get(), e4.get(), e5.get() , str(temperature.get()), str(spoolsize.get()), e7.get(), flipper.get()))
b7.grid(row=1, column=1)

def get_tag(sStatus, id_text, UID1_text, UID2_text, password_text, pack_text):
    b7['state'] = NORMAL
    newUID(sStatus, id_text, UID1_text, UID2_text, password_text, pack_text)

b1=Button(window, text="Get Random NFC Tag", bg='green', width=16, command=lambda: get_tag(sStatus, id_text, UID1_text, UID2_text, password_text, pack_text))
b1.grid(row=1, column=0)

b2=Button(window, text="Use This UID", bg='green', width=16, command=lambda: useUID(sStatus, int(e1.get())))
b2.grid(row=12, column=5)


b8=Button(window, text="Program EMUtag", bg='green', width=16, state=DISABLED, command=lambda: notyet(window))
b8.grid(row=12, column=6)

b3=Button(window, text="Search Database" , bg='yellow', width=16, command=lambda: search(sStatus, list1, END,  e1.get(),e2.get(), e3.get(), e4.get(), e5.get(),e6.get() ))
b3.grid(row=13, column=5)

b4=Button(window, text="View All", bg='yellow', width=16, command=lambda: view(sStatus, window, list1, END))
b4.grid(row=13, column=6)

b5=Button(window, text="Update Record", bg='yellow', width=16, command=lambda: myUpdate(sStatus, e1, e2, e3, e4, e5, e6, e7))
b5.grid(row=14, column=5)

b6=Button(window, text="Insert Record", bg='yellow', width=16, command=lambda: myInsert(sStatus, END, e1, e2, e3, e4, e5, e6, e7))
b6.grid(row=14, column=6)

b9=Button(window, text="Exit", bg='green', width=16, command=lambda: myExit(window))
b9.grid(row=15, column=6)

b10=Button(window, text="Delete Record", bg='red', width=16, command=lambda: myDelete(sStatus, e1.get()))
b10.grid(row=15, column=5)

b11=Button(window, text="Clear Input", bg='yellow', width=16, command=lambda: clearEntry(sStatus, END,  e1, e2, e3, e4, e5, e6, e7))
b11.grid(row=0, column=6)

# define Radio Buttons and label
lTemp=Label(window, text="Filament Temperature")
lTemp.grid(row=2, column=0, columnspan=2)

rTempLow = Radiobutton(window, text="190C", value=190, variable = temperature)
rTempLow.grid(row=3, column=0)
temperature.set(210)

rTempHi = Radiobutton(window, text="210C", value=210, variable = temperature)
rTempHi.grid(row=3, column=1)

lSpool=Label(window, text="Spool Size")
lSpool.grid(row=5, column=0, columnspan=2)

rSpool200 = Radiobutton(window, text="200M", value=200, variable = spoolsize)
rSpool200.grid(row=6, column=0)

rSpool300 = Radiobutton(window, text="300M", value=300, variable = spoolsize)
rSpool300.grid(row=6, column=1)
spoolsize.set(200)

#end of window object
window.mainloop()
