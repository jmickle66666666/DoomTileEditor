from Tkinter import *
import omg
import omg.mapedit
import math

class TileItem:
    def __init__(self, x, y, sector):
        self.x = x
        self.y = y
        self.sector = sector
        self.canvas.create_rectangle((0, 0, 32, 32), outline="white")


class TileCanvas(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.canvas = Canvas(self)

        # Layout and config
        self.canvas.config(bg="#222222")
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.dragging = False
        self.last_pos = (0, 0)
        self.scroll_position = [0, 0]
        self.tile_size = 32

        # Event binding
        self.canvas.bind(sequence="<ButtonPress-1>", func=self.on_mouse_down)
        self.canvas.bind(sequence="<Motion>", func=self.on_mouse_move)
        self.canvas.bind(sequence="<ButtonRelease-1>", func=self.on_mouse_up)
        self.canvas.bind_all(sequence="<KeyPress>", func=self.on_key_down)
        self.canvas.bind_all(sequence="<KeyRelease>", func=self.on_key_up)

        # Stuff
        self.build_map(omg.MapEditor(omg.WAD('test.wad').maps["MAP01"]))

        # Cursor
        self.cursor_id = self.canvas.create_rectangle((0, 0, 32, 32),
                                                      dash=(5,5),
                                                      outline="#ddd",
                                                      tag="cursor")

    def build_map(self, omap):
        for l in omap.linedefs:
            v1 = omap.vertexes[l.vx_a]
            v2 = omap.vertexes[l.vx_b]
            self.canvas.create_line(v1.x, v1.y, v2.x, v2.y, fill="#999922", tag="")

    # Event handlers
    def on_key_down(self, event):
        if event.char == " ":
            self.dragging = True

    def on_key_up(self, event):
        if event.char == " ":
            self.dragging = False

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)

    def on_mouse_down(self, event):
        pass

    def on_mouse_up(self, event):
        pass

    def on_mouse_move(self, event):
        move = (event.x - self.last_pos[0], event.y - self.last_pos[1])
        self.last_pos = (event.x, event.y)

        # Cursor
        coords = self.canvas.coords("cursor")
        move_x = event.x - coords[0] - self.scroll_position[0]
        move_y = event.y - coords[1] - self.scroll_position[1]
        self.canvas.move("cursor",
                         math.floor(move_x / self.tile_size) * self.tile_size,
                         math.floor(move_y / self.tile_size) * self.tile_size)

        # Canvas dragging
        if self.dragging:

            self.canvas.scan_mark(0, 0)
            self.canvas.scan_dragto(move[0], move[1], gain=1)
            self.scroll_position[0] += move[0]
            self.scroll_position[1] += move[1]
