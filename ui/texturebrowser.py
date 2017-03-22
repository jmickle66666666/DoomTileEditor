# The UI and functionality for browsing and selecting textures from texture collections
from Tkinter import *
from util import texturecollection
from PIL import ImageTk


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

    def move_to(self, x, y):
        self.canvas.move(self.image_id, x - self.x, y - self.y)
        self.canvas.move(self.text_id, x - self.x, y - self.y)
        self.canvas.move(self.rect_id, x - self.x, y - self.y)
        self.x = x
        self.y = y


# The panel to list all the textures in a single collection
class TextureGrid(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.config(width=200, height=200)

        self.canvas = Canvas(self, width=500, height=500)
        self.canvas.config(bg="#252321")
        self.canvas.pack(side=LEFT)

        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.texture_items = []
        self.row_item_count = 1

        # this is how much space is between items
        self.item_space = 110

        # self.photo = resutil.load_photoimage_resized(res.temp_splash, (100, 100))
        # self.add_item("test1", self.photo)
        # self.add_item("test2", self.photo)
        # self.add_item("test3", self.photo)
        # self.reposition_items()

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
        self.texture_items = []
        for t in tc.textures:
            thumbnail = tc.textures[t].resize((100, 100))
            photoimage = ImageTk.PhotoImage(thumbnail)
            self.add_item(t, photoimage)
        self.reposition_items()

    def calculate_row_size(self):
        self.row_item_count = max((self.canvas.winfo_reqwidth()+20) // 110, 1)


# A list to show and select one of the currently available texture collections to browse
class TextureCollectionList(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.config(width=200)

        self.junk_text = Label(self, text="TextureCollection 1\nTextureCollection 2\netc")
        self.junk_text.pack()


# The master window for the texture browser
class TextureBrowser(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.title("Texture Browser")
        self.focus_force()

        self.texture_collection_list = TextureCollectionList(self)
        self.texture_collection_list.grid(column=1, row=0, sticky="NS")

        self.texture_grid = TextureGrid(self)
        self.texture_grid.grid(column=0, row=0, sticky="NSEW")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


if __name__ == "__main__":
    test_textures_path = "/Users/jerry.micklethwaite/Dropbox/projects/games/2016/SLDR/metals/"
    tc = texturecollection.TextureCollection.load_folder(test_textures_path)
    app = TextureBrowser(None)
    app.texture_grid.load_texture_collection(tc)
    app.mainloop()
