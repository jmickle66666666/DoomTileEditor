from Tkinter import *
import res
from util import resutil


class SplashScreen(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.splashimage = resutil.load_photoimage(res.temp_splash)
        self.temp_text = Label(self, image=self.splashimage, bg="#333333")
        self.temp_text.photo = self.splashimage
        self.temp_text.pack(fill=BOTH, expand=1)
