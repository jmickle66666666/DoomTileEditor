# UI and data manager for sectors, handles adding/editing/removing sectors.
from tkinter import *
from ui.sectordialogue import SectorDialogue


class SectorManager(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, width=150)

        self.highlighted = 0

        self.sector_frame = Frame(self, width=150)
        self.sector_frame.grid(row=0)

        self.sectors = []

        add_button = Button(self, text="Add Sector", command=self.create_sector)
        add_button.grid(column=0, row=1)

    def update_frame(self):
        self.sector_frame.destroy()
        self.sector_frame = Frame(self, width=150)
        self.sector_frame.grid(row=0)

        for s in self.sectors:
            new_frame = s.get_frame(self.sector_frame, self.highlighted - 1 == self.sectors.index(s))
            new_frame.grid()

    def create_sector(self):
        SectorDialogue(None, self, None, self.add_sector)

    def add_sector(self, sectorinfo):
        self.sectors.append(sectorinfo)
        self.update_frame()

    def export_sectors(self):
        output = []
        for s in self.sectors:
            output.append(s.to_object())
        return output

    def highlight(self, index):
        self.highlighted = index
        self.update_frame()
