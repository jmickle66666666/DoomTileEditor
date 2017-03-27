import random
from tkinter import *
import ui.sectordialogue


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
        ui.sectordialogue.SectorDialogue(None, self.sectormanager, self, self.replace)
