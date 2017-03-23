# Description: UI manager for the main sidebar
from tkinter import Frame
from tkinter.constants import *
from ui.sectormanager import SectorManager


class PropertiesPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.config(border=3, relief=RIDGE, width=150)

        self.sectormanager = SectorManager(self)
        self.sectormanager.grid(column=0, row=1, sticky=NSEW)
