# a TextureCollection contains a dictionary of PIL Images, named depending on texture source
import os
from PIL import Image


class TextureCollection:
    def __init__(self):
        self.textures = {}

    @staticmethod
    def load_folder(path):
        tc = TextureCollection()
        files = os.listdir(path)
        for fp in files:
            try:
                new_img = Image.open(path+fp)
                name = fp[:fp.find(".")]
                tc.textures[name] = new_img
            except IOError:
                pass
        return tc

    @staticmethod
    def load_doom_wad(path):
        pass
