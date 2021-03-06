# a TextureCollection contains a dictionary of PIL Images, named depending on texture source
import os
import omg
import omg.txdef
from PIL import Image


class TextureCollection:
    def __init__(self, name):
        self.textures = {}
        self.name = name

    @staticmethod
    def load_folder(path):
        tc = TextureCollection(path)
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
        tc = TextureCollection(path[path.rfind('/')+1:])
        wad = omg.WAD(path)
        tex = omg.txdef.Textures(wad.txdefs)

        # build the textures out of the patches
        for texturedef in tex:
            new_img = Image.new("RGBA", (tex[texturedef].width, tex[texturedef].height))
            for p in tex[texturedef].patches:
                try:
                    pimg = wad.patches[p.name.upper()].to_Image()
                    pimg = pimg.convert("RGBA")
                    # try and fix transparency issues
                    pixdata = pimg.load()

                    width, height = pimg.size
                    for y in range(height):
                        for x in range(width):
                            if pixdata[x, y] == (255, 0, 255, 255):
                                pixdata[x, y] = (255, 255, 255, 0)

                    new_img.paste(pimg, (p.x, p.y), pimg)
                except:
                    pass
            tc.textures[texturedef] = new_img
        return tc
