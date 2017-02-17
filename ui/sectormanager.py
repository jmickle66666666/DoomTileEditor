# UI and data manager for sectors, handles adding/editing/removing sectors.

from Tkinter import *
import random
import sectordialogue


class SectorInfo:
    def __init__(self, sectormanager):
        self.texture = random.choice(["METAL2", "BIGBRIK2", "SUPPORT2", "FIREBLU1"])
        self.floor = "FLOOR7_1"
        self.ceil = "FLOOR7_2"
        self.z_floor = 0
        self.z_ceil = 128

        self.sectormanager = sectormanager

    def to_object(self):
        output = dict()
        output["texture"] = self.texture
        output["floor"] = self.floor
        output["ceil"] = self.ceil
        output["z_floor"] = self.z_floor
        output["z_ceil"] = self.z_ceil
        return output

    def get_frame(self, parent, highlight=False):
        output = Frame(parent)
        output.config(width=150, height=1)
        if highlight is True:
            output.config(border=1, relief=GROOVE, bg="yellow")

        separator = Frame(output, width=150, height=2, bd=1, relief=SUNKEN)
        separator.grid(column=0, row=0, columnspan=2)

        delete_button = Button(output, text="X", command=self.delete)
        edit_button = Button(output, text="Edit", command=self.edit)

        texture_label = Label(output, text=self.texture, anchor=W)
        floor_label = Label(output, text=self.floor, anchor=W)
        ceil_label = Label(output, text=self.ceil, anchor=W)

        texture_label.grid(column=0, row=1)
        floor_label.grid(column=0, row=2)
        ceil_label.grid(column=0, row=3)
        delete_button.grid(column=1, row=1)
        edit_button.grid(column=1, row=3)

        texture_label.columnconfigure(0, weight=1)

        return output

    def replace(self, sectorinfo):
        self.texture = sectorinfo.texture
        self.floor = sectorinfo.floor
        self.ceil = sectorinfo.ceil
        self.z_floor = sectorinfo.z_floor
        self.z_ceil = sectorinfo.z_ceil
        self.sectormanager.update_frame()

    def delete(self):
        del self.sectormanager.sectors[self.sectormanager.sectors.index(self)]
        self.sectormanager.update_frame()

    def edit(self):
        sectordialogue.SectorDialogue(None, self.sectormanager, self, self.replace)


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
        sectordialogue.SectorDialogue(None, self, None, self.add_sector)

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
