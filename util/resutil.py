from PIL import Image, ImageTk
from io import BytesIO
import base64


# Returns an Image object from a base64 data defined in res.py
def load_image(data):
    return Image.open(BytesIO(base64.b64decode(data)))


# Returns a Tkinter-compatible PhotoImage from a base64 data
def load_photoimage(data):
    return ImageTk.PhotoImage(load_image(data))
