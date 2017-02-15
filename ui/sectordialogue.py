from Tkinter import *


class SectorDialogue(Tk):
    def __init__(self, parent, sectorinfo=None):
        Tk.__init__(self, parent)
        self.title("Sector")

        self.entry_frame = Frame(self)
        self.button_frame = Frame(self)

        self.texture_label = Label(self.entry_frame, text="Texture:", justify=LEFT, width=10, anchor=W)
        self.floor_label = Label(self.entry_frame, text="Floor:", justify=LEFT, width=10, anchor=W)
        self.ceil_label = Label(self.entry_frame, text="Ceil:", justify=LEFT, width=10, anchor=W)

        self.texture_entry = Entry(self.entry_frame)
        self.floor_entry = Entry(self.entry_frame)
        self.ceil_entry = Entry(self.entry_frame)

        self.save_button = Button(self.button_frame, text="Save")
        self.cancel_button = Button(self.button_frame, text="Cancel")

        # Opened Data
        if sectorinfo is not None:
            self.texture_entry.insert(0, sectorinfo.texture)
            self.floor_entry.insert(0, sectorinfo.floor)
            self.ceil_entry.insert(0, sectorinfo.ceil)

        # Layout
        self.texture_label.grid(column=0, row=0)
        self.floor_label.grid(column=0, row=1)
        self.ceil_label.grid(column=0, row=2)
        self.texture_entry.grid(column=1, row=0)
        self.floor_entry.grid(column=1, row=1)
        self.ceil_entry.grid(column=1, row=2)

        self.save_button.grid(column=1, row=0)
        self.cancel_button.grid(column=2, row=0)

        self.entry_frame.grid(column=0, row=0)
        self.button_frame.grid(column=0, row=1)

if __name__ == "__main__":
    app = SectorDialogue(None)
    app.mainloop()