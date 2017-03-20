from Tkinter import *


class SplashScreen(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.temp_text = Label(self, text="hello")
        self.temp_text.grid(column=0, row=0)
