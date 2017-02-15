from Tkinter import *
import math


class TileItem:
    def __init__(self, tilecanvas, x, y, sector):
        self.x = x
        self.y = y
        self.sector = sector
        self.tilecanvas = tilecanvas
        self.canvas = tilecanvas.canvas
        tilesize_scaled = tilecanvas.tile_size * tilecanvas.scale
        x1 = (x * tilesize_scaled) + self.canvas.coords("anchor")[0]
        y1 = (y * tilesize_scaled) + self.canvas.coords("anchor")[1]
        x2 = x1 + (tilesize_scaled)
        y2 = y1 + (tilesize_scaled)
        self.id = self.canvas.create_rectangle((x1, y1, x2, y2),
                                               outline="white",
                                               fill="#444")

    def destroy(self):
        self.canvas.delete(self.id)


class TileCanvas(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.canvas = Canvas(self)

        # Layout
        self.canvas.config(bg="#222222")
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        # Settings
        self.dragging = False
        self.last_pos = (0, 0)
        self.scroll_position = [0, 0]
        self.mouse_tile = [0, 0]
        self.tiles = []
        self.mouse_down = False
        self.scale = 1.0
        self.max_scale = 10.0
        self.min_scale = 0.1
        self.canvas.create_line(0, 0, 1, 1, tag="anchor")
        self.tile_size = 32
        self.tool = "brush"

        # Event binding
        self.canvas.bind(sequence="<ButtonPress-1>", func=self.on_mouse_down)
        self.canvas.bind(sequence="<Motion>", func=self.on_mouse_move)
        self.canvas.bind(sequence="<ButtonRelease-1>", func=self.on_mouse_up)
        self.canvas.bind_all(sequence="<KeyPress>", func=self.on_key_down)
        self.canvas.bind_all(sequence="<KeyRelease>", func=self.on_key_up)
        self.canvas.bind(sequence="<MouseWheel>", func=self.on_mouse_wheel)

        # Cursor
        self.cursor_id = self.canvas.create_rectangle((0, 0, 32, 32),
                                                      dash=(5, 5),
                                                      outline="#ddd",
                                                      tag="cursor")

    def get_tile(self, x, y):
        for t in self.tiles:
            if t.x == x and t.y == y:
                return t
        return None

    def set_mouse_tile(self, event):
        mpos_x = event.x - self.canvas.coords("anchor")[0]
        mpos_y = event.y - self.canvas.coords("anchor")[1]

        mpos_x = math.floor(mpos_x / (self.tile_size * self.scale))
        mpos_y = math.floor(mpos_y / (self.tile_size * self.scale))

        self.mouse_tile[0] = mpos_x
        self.mouse_tile[1] = mpos_y

    def update_cursor(self, event):
        coords = self.canvas.coords("cursor")
        self.set_mouse_tile(event)
        move_x = ((self.mouse_tile[0] * self.tile_size * self.scale) + self.canvas.coords("anchor")[0]) - coords[0]
        move_y = ((self.mouse_tile[1] * self.tile_size * self.scale) + self.canvas.coords("anchor")[1]) - coords[1]
        self.canvas.move("cursor", move_x, move_y)

    def create_tile_at_cursor(self):
        over_tile = self.get_tile(self.mouse_tile[0], self.mouse_tile[1])
        if over_tile is None:
            self.tiles.append(TileItem(self, self.mouse_tile[0], self.mouse_tile[1], 0))

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
        self.update_cursor(event)
        if self.tool is "brush":
            self.create_tile_at_cursor()
        self.mouse_down = True

    def on_mouse_up(self, event):
        self.update_cursor(event)
        self.mouse_down = False

    def on_mouse_wheel(self, event):
        last_scale = self.scale
        if self.max_scale > (self.scale + (event.delta * 0.1)) > self.min_scale:
            self.scale += (event.delta * 0.1)
            delta = self.scale / last_scale
            self.canvas.scale("all", event.x, event.y, delta, delta)

    def on_mouse_move(self, event):
        move = (event.x - self.last_pos[0], event.y - self.last_pos[1])
        self.last_pos = (event.x, event.y)

        # Cursor
        self.update_cursor(event)

        # Draw Tiles
        if self.mouse_down:
            if self.tool is "brush":
                self.create_tile_at_cursor()

        # Canvas dragging
        if self.dragging:
            self.canvas.move("all", move[0], move[1])
