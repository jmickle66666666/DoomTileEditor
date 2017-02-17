from Tkinter import *
import tkMessageBox
import sectormanager


class SectorDialogue(Tk):
    def __init__(self, parent, sector_manager=None, sectorinfo=None, callback=None):
        Tk.__init__(self, parent)
        self.title("Sector")
        self.focus_force()
        self.resizable(0, 0)

        self.callback = callback
        self.sectormanager = sector_manager
        self.mainframe = Frame(self, padx=10, pady=10)

        self.entry_frame = Frame(self.mainframe)
        self.button_frame = Frame(self.mainframe)
        self.z_frame = Frame(self.mainframe)

        self.texture_label = Label(self.entry_frame, text="Texture:", justify=LEFT, width=9, anchor=W)
        self.floor_label = Label(self.entry_frame, text="Floor:", justify=LEFT, width=9, anchor=W)
        self.ceil_label = Label(self.entry_frame, text="Ceil:", justify=LEFT, width=9, anchor=W)

        self.texture_entry = Entry(self.entry_frame, width=22)
        self.floor_entry = Entry(self.entry_frame, width=22)
        self.ceil_entry = Entry(self.entry_frame, width=22)

        self.z_floor_label = Label(self.z_frame, text="Floor Height:", justify=LEFT, width=9, anchor=W)
        self.z_ceil_label = Label(self.z_frame, text="Ceiling Height:", justify=LEFT, width=10, anchor=W)

        self.z_floor_entry = Entry(self.z_frame, width=5)
        self.z_ceil_entry = Entry(self.z_frame, width=5)

        self.save_button = Button(self.button_frame, text="Save", command=self.save_data, default=ACTIVE)
        self.cancel_button = Button(self.button_frame, text="Cancel", command=self.close)

        # Opened Data
        if sectorinfo is not None:
            self.texture_entry.insert(0, sectorinfo.texture)
            self.floor_entry.insert(0, sectorinfo.floor)
            self.ceil_entry.insert(0, sectorinfo.ceil)
            self.z_floor_entry.insert(0, sectorinfo.z_floor)
            self.z_ceil_entry.insert(0, sectorinfo.z_ceil)

        # Layout
        self.texture_label.grid(column=0, row=0)
        self.floor_label.grid(column=0, row=1)
        self.ceil_label.grid(column=0, row=2)
        self.texture_entry.grid(column=1, row=0)
        self.floor_entry.grid(column=1, row=1)
        self.ceil_entry.grid(column=1, row=2)

        self.z_floor_label.grid(column=0, row=0)
        self.z_ceil_label.grid(column=2, row=0)
        self.z_floor_entry.grid(column=1, row=0)
        self.z_ceil_entry.grid(column=3, row=0)

        self.save_button.grid(column=2, row=0)
        self.cancel_button.grid(column=1, row=0)

        self.entry_frame.grid(column=0, row=0)
        self.z_frame.grid(column=0, row=1)
        self.button_frame.grid(column=0, row=2, sticky=SE, pady=5)

        self.mainframe.grid(column=0, row=2)

    def save_data(self):
        output = sectormanager.SectorInfo(None)
        output.texture = self.texture_entry.get()
        output.floor = self.floor_entry.get()
        output.ceil = self.ceil_entry.get()
        try:
            output.z_floor = int(self.z_floor_entry.get())
            output.z_ceil = int(self.z_ceil_entry.get())
        except ValueError:
            tkMessageBox.showwarning(
                "Value Error!",
                "Floor/Ceiling height is not an integer :("
            )
            return
        output.sectormanager = self.sectormanager
        if self.callback is not None:
            self.callback(output)
        self.close()

    def validate_z_floor(self):
        try:
            int(self.z_floor_entry.get())
            return True
        except ValueError:
            return False

    def validate_z_ceil(self):
        try:
            int(self.z_ceil_entry.get())
            return True
        except ValueError:
            return False

    def close(self):
        self.destroy()


if __name__ == "__main__":
    app = SectorDialogue(None)
    app.mainloop()
