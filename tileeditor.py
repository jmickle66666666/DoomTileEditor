from Tkinter import *
import omg, omg.mapedit

class App(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.geometry("800x600")
        self.canvas = Canvas(self)
        self.canvas.grid(column=0,row=0,sticky="news")
        self.canvas.bind(sequence="<ButtonPress-1>",func=self.blab)
        self.canvas.bind(sequence="<KeyPress-A>",func=self.move_left)
        self.canvas.bind(sequence="<ButtonRelease-1>",func=self.plal)
        self.build_map(omg.MapEditor(omg.WAD('test.wad').maps["MAP01"]))

    def build_map(self,omap):
        for l in omap.linedefs:
            v1 = omap.vertexes[l.vx_a]
            v2 = omap.vertexes[l.vx_b]
            self.canvas.create_line(v1.x,v1.y,v2.x,v2.y)

    def move_left(self, *args): 
        self.canvas.xview -= 10
        print "hard"

    def blab(self, *args):
        self.last_pos = (args[0].x,args[0].y)
        self.canvas.bind(sequence="<Motion>",func=self.parn)

    def plal(self, *args):
        self.canvas.unbind(sequence="<Motion>")

    def parn(self, *args):
        move = (args[0].x - self.last_pos[0], args[0].y - self.last_pos[1])
        self.canvas.scan_mark(0,0)
        self.canvas.scan_dragto(move[0],move[1],gain=1)
        self.last_pos = (args[0].x,args[0].y)


if __name__=="__main__":
    app = App(None)
    app.mainloop()