# The UI and functionality for browsing and selecting textures from texture collections
from tkinter import Tk, Frame, Canvas, Scrollbar
from tkinter.ttk import Treeview
from tkinter.constants import *
from util import texturecollection
from PIL import Image, ImageTk

PREVIEW_SIZE = 100


# A single texture element. A square containing the preview and name of the texture
class TextureItem:
    def __init__(self, name, photoimage, canvas):
        self.x = 0
        self.y = 0
        self.name = name
        self.image = photoimage
        self.canvas = canvas

        text_offset_x = 5
        text_offset_y = 3
        text_bg_color = "#999999"
        highlight_color = "#BBBBBB"

        self.highlight_id = self.canvas.create_rectangle((-2, -2, PREVIEW_SIZE+1, PREVIEW_SIZE+1),
                                                         fill=highlight_color,
                                                         outline=highlight_color)

        self.image_id = self.canvas.create_image((self.x, self.y),
                                                 image=self.image,
                                                 anchor="nw")

        self.text_id = self.canvas.create_text((self.x + text_offset_x, self.y + text_offset_y),
                                               text=name,
                                               anchor="nw")

        self.rect_id = self.canvas.create_rectangle(self.canvas.bbox(self.text_id),
                                                    fill=text_bg_color,
                                                    outline=text_bg_color)

        self.canvas.tag_raise(self.text_id)

        self.unhighlight()

    def move_to(self, x, y):
        self.canvas.move(self.image_id, x - self.x, y - self.y)
        self.canvas.move(self.text_id, x - self.x, y - self.y)
        self.canvas.move(self.rect_id, x - self.x, y - self.y)
        self.canvas.move(self.highlight_id, x - self.x, y - self.y)
        self.x = x
        self.y = y

    def highlight(self):
        self.canvas.itemconfig(self.highlight_id, state=NORMAL)

    def unhighlight(self):
        self.canvas.itemconfig(self.highlight_id, state=HIDDEN)

    def delete(self):
        self.canvas.delete(self.image_id)
        self.canvas.delete(self.text_id)
        self.canvas.delete(self.rect_id)
        self.canvas.delete(self.highlight_id)


# The panel to list all the textures in a single collection
class TextureGrid(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.config(width=200, height=200)

        self.canvas = Canvas(self)
        self.canvas.config(bg="#252321")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind(sequence="<ButtonPress-1>", func=self.on_mouse_down)

        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.bind(sequence="<MouseWheel>", func=self.on_mouse_wheel)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.texture_items = []
        self.row_item_count = 1

        # this is how much space is between items
        self.item_space = PREVIEW_SIZE + 10

    # Add a new texture item
    def add_item(self, name, image):
        self.texture_items.append(TextureItem(name, image, self.canvas))

    # Reposition all the texture items to the current row count
    def reposition_items(self):
        self.calculate_row_size()
        i = 0
        for t in self.texture_items:
            t.move_to((i % self.row_item_count) * self.item_space + 10,
                      (i // self.row_item_count) * self.item_space + 10)
            i += 1

        itemcount = (len(self.texture_items) // self.row_item_count) + 1
        self.canvas.config(scrollregion=(0, 0, 0, 20 + (itemcount * self.item_space)))

    def load_texture_collection(self, tc):
        self.clear_items()
        self.texture_items = []
        for t in tc.textures:
            ratio = float(PREVIEW_SIZE) / max(tc.textures[t].width, tc.textures[t].height)
            thumbnail = tc.textures[t].resize((int(tc.textures[t].width * ratio),
                                               int(tc.textures[t].height * ratio)),
                                              Image.ANTIALIAS)

            photoimage = ImageTk.PhotoImage(thumbnail)
            self.add_item(t, photoimage)
        self.reposition_items()

    def clear_items(self):
        for t in self.texture_items:
            t.delete()
            del t

    def calculate_row_size(self):
        self.row_item_count = max((self.canvas.winfo_width()+20) // self.item_space, 1)

    def on_resize(self, event):
        self.config(width=event.width, height=event.height)
        self.reposition_items()

    def on_mouse_down(self, event):
        c_x = min(event.x // self.item_space, self.row_item_count-1)
        c_y = self.canvas.canvasy(event.y) // self.item_space
        texture_index = int((c_y * self.row_item_count) + c_x)

        # here: iterate the texture items and highlight correct one
        for i, t in enumerate(self.texture_items):
            if i == texture_index:
                t.highlight()
            else:
                t.unhighlight()

        print(self.texture_items[texture_index].name)

    def on_mouse_wheel(self, event):
        self.canvas.yview("scroll", -event.delta, "units")


# A list to show and select one of the currently available texture collections to browse
class TextureCollectionList(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.config(width=200)

        self.collections = []

        self.collection_list = Treeview(self, selectmode="browse")
        self.collection_list.heading("#0", text="Texture Collections")
        self.collection_list.bind("<<TreeviewSelect>>", self.on_select)
        self.collection_list.pack(fill=Y, expand=1)

    def add_collection(self, texture_collection):
        self.collections.append(texture_collection)
        new_id = self.collection_list.insert('', "end")
        self.collection_list.item(new_id, text=texture_collection.name)

    def on_select(self, event):
        selection_id = self.collection_list.selection()[0]
        index = self.collection_list.index(selection_id)
        self.parent.texture_grid.load_texture_collection(self.collections[index])


# The master window for the texture browser
class TextureBrowser(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.title("Texture Browser")
        self.geometry("800x600")
        self.focus_force()

        self.texture_collection_list = TextureCollectionList(self)
        self.texture_collection_list.grid(column=1, row=0, sticky="NS")

        self.texture_grid = TextureGrid(self)
        self.texture_grid.grid(column=0, row=0, sticky="NSEW")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


if __name__ == "__main__":
    app = TextureBrowser(None)
    test_textures_path = "/Users/jerry.micklethwaite/Documents/doom/DOOM2.WAD"
    tc = texturecollection.TextureCollection.load_doom_wad(test_textures_path)
    app.texture_collection_list.add_collection(tc)
    test_textures_path = "/Users/jerry.micklethwaite/Documents/doom/freedoom-0.10.1/freedoom1.wad"
    tc = texturecollection.TextureCollection.load_doom_wad(test_textures_path)
    app.texture_collection_list.add_collection(tc)
    test_textures_path = "/Users/jerry.micklethwaite/Downloads/btsx_e1/btsx_e1a.wad"
    tc = texturecollection.TextureCollection.load_doom_wad(test_textures_path)
    app.texture_collection_list.add_collection(tc)
    test_textures_path = "/Users/jerry.micklethwaite/Downloads/btsx_e1/btsx_e1b.wad"
    tc = texturecollection.TextureCollection.load_doom_wad(test_textures_path)
    app.texture_collection_list.add_collection(tc)
    app.mainloop()
