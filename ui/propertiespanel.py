# Description: UI manager for the main sidebar
from Tkinter import *
import sectormanager


class PropertiesPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.config(border=3, relief=RIDGE, width=150)

        self.sectormanager = sectormanager.SectorManager(self)
        self.sectormanager.grid(column=0, row=1, sticky=NSEW)
