#myFunctions.py - function program for the daVinciJrTagManager set up programs
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

import  csv
from SQLbackend import connect, insert, delete, update
from tkinter import *
import textwrap

def notyet(window):
    tkMessageBox.showinfo(title="Function Not Supported", message='Sorry, I have not implimented this function yet')
    return

def myExit(window2close):
    print("See ya later, Alligator")
    window2close.quit()

def myDelete(status, oid):
    mDelete = tkMessageBox.askyesno(title="Delete Record", message='Are you sure?')
    if mDelete > 0:
        delete(status, oid)
        return

def dbCreateUpdate(status, window, FD):

    status.set("Status: This may take awhile")

    #now lets open the csv file and  create / update  the database
    fname= FD.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    connect()
    with open(fname, 'rb') as csvfile:
        for line in csvfile.readlines():
            print(line)
            array = line.split(',')
            if array[0] == "4" or array[0] =="04":                      # first byte must be 4
                for x in range(0 , len(array)):
                    if len(array[x] ) ==  1:
                        array[x] = '0' + array[x]  # make sure there are 2 characters

                UID1 = array[0]  + array[1] + array[2]
                UID2 = array[3]  + array[4] + array[5] + array[6]
                Pword = array[8]  + array[9] + array[10] + array[11]
                tempPACK= array[13]  + array[14]
                Used = ""
                PACK = tempPACK.rstrip()
                # Use only if there is a PACK valid -> Record is valid
                if PACK:
                    print('data ok')
                    insert(status, UID1.rstrip(), UID2.rstrip(), Pword.rstrip(), PACK.rstrip(), Used)
    status.set("Status: Database updated")


def onselect(evt, id, uid1, uid2, pword, pack, used):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    id.set(value[0])
    uid1.set(value[1])
    uid2.set(value[2])
    pword.set(value[3])
    pack.set(value[4])
    used.set(value[5])


def generateTagData(status, uid1, uid2, pword, pack, temperature, spoolsize, page9, flipper):
    #Page  300m/300m        200m/200/       PLA/190*        PLA/210*
    #10,11 E0930400         400D0300
    #20    E0930400         400D0300
    #21    A8813654         081F3154
    #22    F03FEECE         50B1E0CE
    #23    F26E4D76         52E74F76
    #08                                     5A504800    5A504F00

    word = ['04A0B961', '229A3D80', '79480000', 'E1101200', '0103A00C', '340300FE', '00000000', '00000000',
            '5A505A00', '0035344A', 'E0930400', 'E0930400', 'D2002D00', '54484742', 'E09304FF', '00000000',
            '00000000', '34000000', '00000000', '00000000', 'E0930400', 'A8813654', 'F03FEECE', 'F26E4D76',
            '00000000', '00000000', '00000000', '00000000', '00000000', '000000FF', '00000000', '00000000',
            '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000',
            '000000BD', '070000FF', '80050000', '0D02FB70', '6B680000']
    word[0] = (uid1 + "AA").rstrip()
    word[1] = uid2.rstrip()
    if temperature == "210":
        print("temperature = 210")
        word[8] = '5A504F00'
    if spoolsize == "200":
        print("Spoolsize = 200")
        word[10] = '400D0300'
        word[11] = '400D0300'
        word[20] = '400D0300'
        word[21] = '081F3154'
        word[22] = '50B1E0CE'
        word[23] = '52E74F76'
    if page9 != "":
        print("updating page 9")
        word[9] = page9
    word[43] = pword.rstrip()
    word[44] = (pack + "0000").rstrip()

    #Write the data to the file
    # we need only a \n = 0A = chr(10) for the line termination
    # character.  In windows it will put \r\n.  Using chr(10) to
    #force only the 0A.  Also, do not want it on the last line
    # Word is 45 pages 0 based so it is 0-44.  sub 1 from len(word)
    # to get last page  The resulting txt file is 404 bytes
    fname=uid1 + 'filament.nfc'
    if not flipper:
        fname=uid1 + 'tagdata.txt'
    f1=open(fname, 'w')
    if not flipper:
        for x in range(len(word)-1):
            f1.write(word[x]  + chr(10))
        f1.write(word[len(word)-1])
    else:
        header = """Filetype: Flipper NFC device
Version: 3
# Nfc device type can be UID, Mifare Ultralight, Mifare Classic, Bank card
Device type: NTAG213
# UID, ATQA and SAK are common for all formats
"""
        header += "UID: " + ' '.join([uid1[j:j+2] for j in range(0, len(uid1), 2)]) + ' ' + ' '.join([uid2[j:j+2] for j in range(0, len(uid2), 2)]) + "\n"
        header += """ATQA: 00 44
SAK: 00
# Mifare Ultralight specific data
Data format version: 1
Signature: DE AD BE EF DE AD BE EF DE AD BE EF DE AD BE EF DE AD BE EF DE AD BE EF DE AD BE EF DE AD BE EF
Mifare version: 00 04 04 04 01 00 0F 03
Counter 0: 0
Tearing 0: 00
Counter 1: 0
Tearing 1: 00
Counter 2: 0
Tearing 2: 00
Pages total: 45
Pages read: 45\n"""
        f1.write(header)
        for i, line in enumerate(word):
            # Split the line into pairs of hex characters
            hex_pairs = [line[j:j+2] for j in range(0, len(line), 2)]
            # Format the page output
            f1.write(f"Page {i}: {' '.join(hex_pairs)}\n")
        f1.write("Failed authentication attempts: 0")
    f1.close()
    status.set("Status: New tag data written as " + fname)


def clearEntry(sStatus, END, id, uid1, uid2, pword, pack, used, page9):
    id.delete(0,END)
    uid1.delete(0,END)
    uid2.delete(0,END)
    pword.delete(0,END)
    pack.delete(0,END)
    used.delete(0,END)
    page9.delete(0,END)

def is_hex(*args):
    ans = True
    for arg in args:
        if not arg=='':
            try:
                int(arg, 16)
            except ValueError:
                ans =  False
    if ans == False:
        return False
    else:
        return True

def myUpdate(status, id, uid1, uid2, pword, pack, used, page9):
    if len(uid1.get()) == 6 and len(uid2.get()) ==8 and len(pword.get()) ==8 and len(pack.get()) ==4:
        if is_hex(uid1.get(), uid2.get(), pword.get(), pack.get()):
            update(status, id.get(), uid1.get(), uid2.get(), pword.get(), pack.get(), used.get())
            clearEntry(status, END, id, uid1, uid2, pword, pack, used, page9)
        else:
            tkMessageBox.showwarning("Warning", "One entry in UID-1, UID-2, Password, PACK  is not hex")
    else:
        tkMessageBox.showwarning("Warning", "One entry in UID-1, UID-2, Password, PACK  length is incorrect")

def myInsert(status, END, id, uid1, uid2, pword, pack, used, page9):
    if len(uid1.get()) == 6 and len(uid2.get()) ==8 and len(pword.get()) ==8 and len(pack.get()) ==4:
        if is_hex(uid1.get(), uid2.get(), pword.get(), pack.get()):
            insert(status, uid1.get(), uid2.get(), pword.get(), pack.get(), used.get())
            clearEntry(status, END, id, uid1, uid2, pword, pack, used, page9)
        else:
            tkMessageBox.showwarning("Warning", "One entry in UID-1, UID-2, Password, PACK  is not hex")
    else:
        tkMessageBox.showwarning("Warning", "One entry in UID-1, UID-2, Password, PACK  length is incorrect")
##########################3  Below added for help window ###################
def raise_window(window):
    window.attributes('-topmost', 1)
    window.attributes('-topmost', 0)

# Destroy window
def destroy_help_window(window2destroy):
    window2destroy.destroy()

# Displays help text in the text box
def whatText(where, what):
    where.delete(1.0,END)
    for btn in what:
        dedented_text = textwrap.dedent(btn).strip()
        final_text = textwrap.fill(dedented_text, initial_indent='', subsequent_indent='     ')
        where.insert(END, final_text)
        where.insert(END, '\n')

def myHelp():
# Create new top level window. Opens immediately
    help_window = Toplevel()
    help_window.title('da Vinci Tag Manager Help')
    help_window.geometry("615x300")
    raise_window(help_window)
    help_window.focus_force()

#create a button frame
    button_frame = Frame(help_window)
    button_frame.pack()

# add seperator / frame
    separator = Frame(help_window, height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X, padx=5, pady=5)

# help window focus
    help_scroll = Scrollbar(help_window)
    help_text = Text(help_window, height=10, width=70, wrap=WORD, borderwidth=5, padx=10)
    help_scroll.pack(side=RIGHT, fill=Y)
    help_text.pack(side=LEFT, fill=Y)
    help_scroll.config(command=help_text.yview)
    help_text.config(yscrollcommand=help_scroll.set)
    h_text = []
    h_text.append("Welcome to the daVinci Tag Manager.  This program will allow you \
to create a text file that you can then use your andriod phone to program your \
EMUtag, and also track which UID / Passwod / PACK code you already used.")
    h_text.append("The current database contains over 400 UID / Passwod / PACK entries, all gathered \
from the Soliforum and the cvs file that CGRILLO maintains.")
    h_text.append("Please be aware of some limitations:")
    h_text.append("There is  input validation on the UID-1, UId-2, Password and PACK.  We check both the length \
and make sure that theey are hexidecimal.  The id field is a decimal.  The Used field is \
anything you want, it will be prepopulated with 'Used - <todays date>' when you select Use This UID button.  ALL others \
are hexidecimal.")
    h_text.append("The lentgh of the field varies.  UID-1 is 3 bytes of HEX data.  UID-2 and Password are 4 bytes of HEX data \
and the PACK is 2 bytes of Hex.")
    h_text.append("Page9 data is not populated or suggested.  If you need to populate it ( I have not needed to \
do it), it is 4 HEX bytes.  The forums say 'First two bytes are always 00. Last three bytes are part of the spools \
serial number when converted to ASCII.'  Page 9 data is not saved in the database, but is put in the tagdata file")
    i_text = []
    i_text.append("Starting a new database or importing more data in the existing one is easy.  Just select File , then Create or Update Database \
from the menu bar.")
    i_text.append("A file dialogue box will open asking you to select the CSV file to open and import.")
    i_text.append("VERY IMPORTANT....")
    i_text.append("It MUST be the CSV file that is in the Soliforum, currently maintained by CGRILLO and is located in post #1 \
 here: http://www.soliforum.com/topic/15817/davinci-jr-and-mini-nfc-password-requests/  .  That file format, with the current layout \
 is hard coded into the create / import function")
    i_text.append("Just choose the file, select ok, and it will import it.  While importing it will check for a PACK code and if present \
we assume it is valid.  No PACK code, the entry is skipped.")
    i_text.append("Duplicate entries are also skipped, meaning if you import the file months later after it has grown, existing entries will \
not be imported")
    i_text.append("Please note that the current database contains 427 records.  That should last for awhile")
    g_text = []
    g_text.append("The simpliest way to use this program is to use the GREEN buttons.")
    g_text.append("First,  Press Get New UID.  This will populate the input fields with the first unused UID.")
    g_text.append("Then press Use This UID.  This will mark the UID as 'Used - <todays date>' in the database.")
    g_text.append("Now select the Filament Temperature and Spool Size.")
    g_text.append("Now press Generate Tagdata.")
    g_text.append("This will create a text file, the name starting with UID-1, in the current directory.")
    g_text.append("Now press Exit to exit the program.")
    g_text.append("Whats left for you to do is transfer the tagdata file you just created \
to your phone.  Using the Android app, MIFARE++ Ultralight, program your EMUtag.  Thats it. \
You're good to go.")
    y_text = []
    y_text.append("The yellow buttons are for database management and searching.  With them you can find used tags, search for a \
specific UID or PACK, update and add new records as they are available.  We will go over each button.")
    y_text.append("Clear Input will clear all the fields under the button.  It does not reset Filament Temperature or Spool Size.")
    y_text.append("Search Database will do an OR function on the id, UID-1, UID-2, Password and PACK data. So if you enter data\
in all of those fields, you will get all records matching the id, the UID-1, etc...  It will not narrow the\
results, but rather create more.  If you want to find the used tages, put the search criteria in the Used filed and search.")
    y_text.append("View All will display all the records in the results box.")
    y_text.append("Update Record will change the record that you have altered in the input boxes.  You must have the id to \
update the record. The usual use for this is adding a PACK code to a record you have already entered.")
    y_text.append("Insert Record will create a new record in the database. ")
    y_text.append("Search Results box.  If you have search results showing in the Search Results box, selecting one ( by clicking it ) will populate the fields above.")
    y_text.append("Status Line at the bottom will keep you up to date as to what is happening. ")

    whatText(help_text, h_text)
# put buttons here so they know stuff
    intro_button = Button(button_frame,  bg='white', text='Introduction',  command=lambda: whatText(help_text, h_text)  )
    intro_button.pack(side=LEFT)
    import_button = Button(button_frame,  bg='cyan', text='Tell me how to import',  command=lambda: whatText(help_text, i_text) )
    import_button.pack(side=LEFT)
    green_button = Button(button_frame,  bg='green', text='Tell me about green',  command=lambda: whatText(help_text, g_text)   )
    green_button.pack(side=LEFT)
    yellow_button = Button(button_frame,  bg='yellow', text='Tell me about yellow',  command=lambda: whatText(help_text, y_text)    )
    yellow_button.pack(side=LEFT)
    close_button = Button(button_frame,  bg='magenta',text='Close this help window',  command=lambda: destroy_help_window(help_window)  )
    close_button.pack(side=LEFT)


def myHelpAbout():
# Create new top level window. Opens immediately
    helpAbout_window = Toplevel()
    helpAbout_window.title('About: da Vinci Tag Manager')
    helpAbout_window.geometry("615x300")
    raise_window(helpAbout_window)
    helpAbout_window.focus_force()

#create a button frame
    button_frame = Frame(helpAbout_window)
    button_frame.pack()

# add seperator / frame
    separator = Frame(helpAbout_window, height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X, padx=5, pady=5)

# help window focus
    helpAbout_scroll = Scrollbar(helpAbout_window)
    helpAbout_text = Text(helpAbout_window, height=10, width=70, wrap=WORD, borderwidth=5, padx=10)
    helpAbout_scroll.pack(side=RIGHT, fill=Y)
    helpAbout_text.pack(side=LEFT, fill=Y)
    helpAbout_scroll.config(command=helpAbout_text.yview)
    helpAbout_text.config(yscrollcommand=helpAbout_scroll.set)
    h_text = []
    h_text.append("daVinci Jr Tag Manager is licensed under the GNU General \
Public License v3.0 Permissions of this strong copyleft license are conditioned on making \
available complete source code of licensed works and modifications, which include larger \
works using a licensed work, under the same license. Copyright and license notices must \
be preserved. Contributors provide an express grant of patent rights.")
    h_text.append("Copyright (C) 2017  Mark Ferrick (MJF55) ")

    whatText(helpAbout_text, h_text)
# put buttons here so they know stuff
    close_button = Button(button_frame,  text='Close this window',  command=lambda: destroy_help_window(helpAbout_window)   )
    close_button.pack(side=LEFT)
