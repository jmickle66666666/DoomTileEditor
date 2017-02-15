from Tkinter import *
import tilecanvas
import tile2doom


class App(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.geometry("800x600")
        self.tilecanvas = tilecanvas.TileCanvas(self)
        self.tilecanvas.grid(column=0, row=0, sticky=NSEW)
        self.tilecanvas.columnconfigure(0, weight=1)
        self.tilecanvas.rowconfigure(0, weight=1)

        self.save_button = Button(self, text="save", command=self.save_onclick)
        self.save_button.grid(column=0, row=1)
        self.tilecanvas.rowconfigure(0, weight=0)

    def save_onclick(self):
        data = dict()
        data["version"] = "0.1"
        data["tiles"] = self.tilecanvas.export_tiles()
        data["width"] = self.tilecanvas.get_width()
        data["height"] = self.tilecanvas.get_height()
        data["format"] = "coords"
        data["tilesize"] = self.tilecanvas.tile_size
        data["void"] = 0
        data["sectors"] = [{"texture": "METAL2",
                            "floor": "FLOOR7_1",
                            "ceil": "F_SKY1",
                            "z_floor": 0,
                            "z_ceil": 128},
                           {"texture": "BIGBRIK2",
                            "floor": "FLAT5",
                            "ceil": "FLOOR7_2",
                            "z_floor": 8,
                            "z_ceil": 112}]
        print data
        owad = tile2doom.json2doom(data)
        owad.to_file("output.wad")

if __name__ == "__main__":
    app = App(None)
    app.mainloop()
