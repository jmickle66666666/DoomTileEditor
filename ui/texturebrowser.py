# The UI and functionality for browsing and selecting textures from texture collections
from Tkinter import *
import res
from util import resutil


# A single texture element. A square containing the preview and name of the texture
class TextureItem(Frame):
    def __init__(self, parent, name, photoimage):
        Frame.__init__(self, parent)

        self.image_label = Label(self, image=photoimage, width=100, height=100)
        self.image_label.photo = photoimage
        self.image_label.pack(expand=0)

        self.name_label = Label(self, text=name, width=100)
        self.name_label.pack(expand=0)


# The panel to list all the textures in a single collection
class TextureGrid(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.config(width=200, height=200, bg="#555555", bd=2, relief=SUNKEN)

        self.splashimage = resutil.load_photoimage(res.temp_splash)
        self.test_item = TextureItem(self, "testname", self.splashimage)
        self.test_item.pack()


# A list to show and select one of the currently available texture collections to browse
class TextureCollectionList(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.config(width=200, bg="#333333")


# The master window for the texture browser
class TextureBrowser(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.title("Texture Browser")
        self.focus_force()

        self.texture_collection_list = TextureCollectionList(self)
        self.texture_collection_list.grid(column=1, row=0, sticky=NS)

        self.texture_grid = TextureGrid(self)
        self.texture_grid.grid(column=0, row=0, sticky="NSEW")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


if __name__ == "__main__":
    print "1"
    app = TextureBrowser(None)
    app.mainloop()
