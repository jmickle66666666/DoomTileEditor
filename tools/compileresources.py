# This script will compile all the files in the res/ folder into base64 data in res.py for embedding directly into the
# application

import os
import base64

files = os.listdir("../res/")
encodes = []

for fn in files:
    with open("../res/"+fn) as f:
        encodes.append(base64.b64encode(f.read()))

if os.path.isfile("../res.py"):
    os.remove("../res.py")

with open("../res.py", "w") as f:
    for i in range(len(encodes)):
        name = files[i][:files[i].find(".")]
        print("writing {}".format(name))
        f.write("{} = \"{}\"\n\n".format(name, encodes[i]))
