# Description: Main UI window and entry point for the application
from tkinter import Tk, Menu
from tkinter.constants import *
from ui import propertiespanel
from ui import tilecanvas
from ui import splashscreen
from util import tile2doom


class App(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.geometry("800x600")
        self.title("DoomTileEditor")
        self.focus_force()

        self.tilecanvas = None
        self.propertiespanel = None
        self.sectormanager = None
        self.splashscreen = None
        self.menubar = None
        self.file_menu = None

        self.init_menubar()
        self.splash_screen()

    def save_map(self):
        data = dict()
        data["version"] = "0.1"
        data["tiles"] = self.tilecanvas.export_tiles()
        data["width"] = self.tilecanvas.get_width()
        data["height"] = self.tilecanvas.get_height()
        data["format"] = "coords"
        data["tilesize"] = self.tilecanvas.tile_size
        data["void"] = 0
        data["sectors"] = self.sectormanager.export_sectors()
        owad = tile2doom.json2doom(data)
        owad.to_file("output.wad")

    def new_map(self):
        self.close_splash()

        self.propertiespanel = propertiespanel.PropertiesPanel(self)
        self.propertiespanel.pack(fill=BOTH, side=RIGHT)

        self.sectormanager = self.propertiespanel.sectormanager

        self.tilecanvas = tilecanvas.TileCanvas(self)
        self.tilecanvas.pack(fill=BOTH, expand=1, side=LEFT)

        self.pack_propagate(False)

        self.enable_map_menu_options()

    def splash_screen(self):
        self.splashscreen = splashscreen.SplashScreen(self)
        self.splashscreen.pack(fill=BOTH, expand=1)
        self.disable_map_menu_options()

    def close_map(self):
        self.propertiespanel.destroy()
        self.tilecanvas.destroy()
        self.splash_screen()
        self.disable_map_menu_options()

    def close_splash(self):
        self.splashscreen.destroy()

    def enable_map_menu_options(self):
        self.file_menu.entryconfig("Save map", state="normal")
        self.file_menu.entryconfig("Close map", state="normal")

    def disable_map_menu_options(self):
        self.file_menu.entryconfig("Save map", state="disabled")
        self.file_menu.entryconfig("Close map", state="disabled")

    def init_menubar(self):
        self.menubar = Menu(self)
        self.file_menu = Menu(self)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New map", command=self.new_map)
        self.file_menu.add_command(label="Save map", command=self.save_map)
        self.file_menu.add_command(label="Close map", command=self.close_map)
        self.file_menu.add_command(label="Quit", command=self.quit)
        self.config(menu=self.menubar)


if __name__ == "__main__":
    app = App(None)
    app.mainloop()
