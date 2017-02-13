from Tkinter import *
import omg
import omg.mapedit
import tilecanvas


class App(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.geometry("800x600")
        self.tilecanvas = tilecanvas.TileCanvas(self)
        self.tilecanvas.pack(fill=BOTH, expand=YES)
        self.tilecanvas.columnconfigure(0,weight=1)


if __name__ == "__main__":
    app = App(None)
    app.mainloop()
