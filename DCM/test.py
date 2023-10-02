from tkinter import * # Main Tkinter Module Import
from tkinter import ttk #Ttk Module Import (provides modern themed widget set and API)
root = Tk() #Initialize TK widget and create root window (main window of the application)
frm = ttk.Frame(root, padding = 10) #Create frame widget inside of main window (like a table in HTML)
frm.grid() #Specify relative layout/position of the objects put inside the frame
ttk.Label(frm, text = "Hello World!").grid(column=0,row=0) #Create Label Saying Hello World and Place it in on Top Left (First Row, First Column)
ttk.Button(frm, text = "Quit", command=root.destroy).grid(column=1,row=0) #Create Quit Button to Exit Application and Place it on Top Right (First Row, Second Column)
root.mainloop() #This puts everything on the display and responds to user input until the program terminates