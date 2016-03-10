from WhacmeWindow import *
import Tkinter as tk

ALL='nsew'

root = tk.Tk()
root.grid()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


w = WhacmeWindow(root)
w.grid(sticky=ALL)

root.mainloop()
