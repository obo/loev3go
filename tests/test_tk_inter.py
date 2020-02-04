#!/usr/bin/env python3
# this is a very simple test whether tkinter is working well
# tkinter got corrupted on my SD card and immediately crashed
# loev3go needs tkinter for the canvas, to preview drawings in SVG
from tkinter import *
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
root = Tk()
app = Window(root)
root.mainloop()
