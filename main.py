from WhacmeWindow import *
import Tkinter as tk

ALL='nsew'

root = tk.Tk()
root.grid()
root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# not the defaults
w = WhacmeWindow(parent=root, mainColor='#fff4ea', mainDarkColor='#99724c', mainHighlightColor='#eec69e',\
							  sideColor='#ffeaff', sideDarkColor='#994c99', sideHighlightColor='#ee9eee')
# uses the defaults
ww = WhacmeWindow(root)


w.grid(row=0, column=0, sticky=ALL)
ww.grid(row=0, column=1, sticky=ALL)

root.mainloop()
