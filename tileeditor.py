# Description: Main UI window and entry point for the application

from Tkinter import *

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

        self.new_map()
        self.close_map()

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
        self.propertiespanel = propertiespanel.PropertiesPanel(self, self.save_map)
        self.propertiespanel.pack(fill=BOTH, side=RIGHT)

        self.sectormanager = self.propertiespanel.sectormanager

        self.tilecanvas = tilecanvas.TileCanvas(self)
        self.tilecanvas.pack(fill=BOTH, expand=1, side=LEFT)

        self.pack_propagate(False)

    def splash_screen(self):
        self.splashscreen = splashscreen.SplashScreen(self)
        self.splashscreen.pack(fill=BOTH)

    def close_map(self):
        self.propertiespanel.destroy()
        self.tilecanvas.destroy()
        self.splash_screen()

if __name__ == "__main__":
    app = App(None)
    app.mainloop()
