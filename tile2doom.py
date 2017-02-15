import omg, random, json
from PIL import Image

# global var for how big the tiles need to be
TILESIZE = 32

# MapSector class, stores the sector information for each tile
class MapSector:
    def __init__(self, sidedef, floor, ceil, z_floor, z_ceil):
        self.sidedef = sidedef
        self.floor = floor
        self.ceil = ceil
        self.z_floor = z_floor
        self.z_ceil = z_ceil

    # returns a new doom format sidedef, using the texture defined
    def get_sidedef(self):
        return omg.mapedit.Sidedef(tx_mid=self.sidedef)

    # returns a new doom format sector, using the flats and z_ heights defined
    def get_sector(self):
        return omg.mapedit.Sector(tx_ceil=self.ceil,tx_floor=self.floor,z_ceil=self.z_ceil,z_floor=self.z_floor)

# convert an image to a set of tiles, using unique colors as indexes. useful for testing, not in practice :)
def image_to_tiles(img):
    print "converting image to tiles..."
    pix = img.load()

    # scan colors in the image first
    colors = []
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            colors.append(pix[i,j])
    # remove duplicates
    colors = sorted(list(set(colors)))
    
    output = [[-1 for y in range(img.size[0])] for x in range(img.size[1])]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            output[i][j] = colors.index(pix[i,j])
    return output
    
# test function to generate a set of tiles
def gentiles():
    width = 30
    height = 30
    tiles = [[-1 for y in range(width)] for x in range(height)]
    def digger(i,j):
        length = 80
        sid = random.choice([0,1,2,3])
        while length > 0:
            tiles[i][j] = 0
            tiles[i+1][j] = 0
            tiles[i][j+1] = 0
            tiles[i+1][j+1] = 0
            length -= 1
            if sid == 0: i += 1
            if sid == 1: j -= 1
            if sid == 2: i -= 1
            if sid == 3: j += 1
            if random.choice([0,0,0,1]) == 1:
                sid += random.choice([-1,1])
                if sid == 4: sid = 0
                if sid == -1: sid = 3
        return (i,j)
    last = digger(15,15)

    for i in range(1, width-1):
        for j in range(1, height-1):
            if tiles[i][j] == -1:
                if tiles[i+1][j] == 0: tiles[i][j] = 1
                if tiles[i-1][j] == 0: tiles[i][j] = 1
                if tiles[i][j+1] == 0: tiles[i][j] = 1
                if tiles[i][j-1] == 0: tiles[i][j] = 1

    return tiles

# Line class for use before converting into a doom format line
class MapLine:
    def __init__(self,x1,y1,x2,y2,front,back):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.front = front
        self.back = back
        self.remain = True
        # this is for line merging, if its a cardinal direction store a value, otherwise
        # just make sure two lines don't get merged automatically. not a cool method
        self.angle = random.random()
        if self.x1 == self.x2 and self.y1 < self.y2: self.angle = 0
        if self.x1 == self.x2 and self.y1 > self.y2: self.angle = 1
        if self.y1 == self.y2 and self.x1 < self.x2: self.angle = 2
        if self.y1 == self.y2 and self.x1 > self.x2: self.angle = 3

    # return tuples of the position
    def v1(self):
        return (self.x1,self.y1)

    def v2(self):
        return (self.x2,self.y2)

    # check if two lines share a point, but not the same point!
    @staticmethod
    def share_a_point(l1,l2):
        if l1.v1() == l2.v2(): return True
        # if l1.v1() == l2.v1(): return True
        if l1.v2() == l2.v1(): return True
        # if l1.v2() == l2.v2(): return True
        return False

    # create a new line, merging the two
    @staticmethod
    def merged_line(l1,l2):
        newline = None
        if l1.v2() == l2.v1(): 
            newline = MapLine(l1.x1,l1.y1,l2.x2,l2.y2,l1.front,l1.back)
        elif l1.v1() == l2.v2(): 
            newline = MapLine(l2.x1,l2.y1,l1.x2,l1.y2,l1.front,l1.back)
        
        return newline

# convert tile data into linedata, ready for writing to a doom map
def tiles2linedata(tiles, void):
    # convert the tiles from tiles to lines defining the edges of the tiles
    # the lines will thus informations: x1, y1, x2, y2, front index, back index
    maplines = []

    # create the lines in all the different situations we need
    # edges of the tilemap are handled separately 
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if i == 0 and tiles[i][j] != void:
                # edge left
                maplines.append(MapLine( 0, (j * TILESIZE), 0, (j*TILESIZE)+TILESIZE, tiles[i][j], void))
            if j == 0 and tiles[i][j] != void:
                # edge bottom
                maplines.append(MapLine( (i*TILESIZE)+TILESIZE, 0, (i*TILESIZE), 0, tiles[i][j], void))
            if i == len(tiles)-1:
                if tiles[i][j] != void:
                    # edge right
                    maplines.append(MapLine( (i*TILESIZE)+TILESIZE, (j*TILESIZE)+TILESIZE, (i*TILESIZE)+TILESIZE, (j*TILESIZE), tiles[i][j], void))
            elif tiles[i][j] != tiles[i+1][j]:
                # vertical
                if tiles[i][j] != void:
                    maplines.append(MapLine( (i*TILESIZE) + TILESIZE, (j*TILESIZE) + TILESIZE, (i*TILESIZE) + TILESIZE, (j*TILESIZE) , tiles[i][j], tiles[i+1][j] ))
                else:
                    maplines.append(MapLine( (i*TILESIZE) + TILESIZE, (j*TILESIZE), (i*TILESIZE) + TILESIZE, (j*TILESIZE) + TILESIZE, tiles[i+1][j], void ))
            if j == len(tiles[i])-1:
                if tiles[i][j] != void:
                    # edge top
                    maplines.append(MapLine( (i*TILESIZE), (j*TILESIZE)+TILESIZE, (i*TILESIZE) +TILESIZE, (j*TILESIZE)+TILESIZE, tiles[i][j], void))
            elif tiles[i][j] != tiles[i][j+1]:
                # horizontal
                if tiles[i][j] != void:
                    maplines.append(MapLine( (i*TILESIZE) , (j*TILESIZE) + TILESIZE, (i*TILESIZE) +TILESIZE, (j*TILESIZE) + TILESIZE, tiles[i][j], tiles[i][j+1] ))
                else:
                    maplines.append(MapLine( (i*TILESIZE)+TILESIZE, (j*TILESIZE) + TILESIZE, (i*TILESIZE), (j*TILESIZE) + TILESIZE, tiles[i][j+1], void ))

    print "merge lines"
    # merge lines

    mergeone = True # we break out of the loop every time we create a line, this is necessary to make sure it works
    timeout = 1000 # just in case. might get rid of this since it works now
    print "map lines at start: {}".format(len(maplines)) # lets see how many lines we saved! spoilers: a lot
    while mergeone is True and timeout > 0:
        #print timeout
        timeout -= 1 
        mergeone = False
        for l1 in maplines:
            if mergeone is True: break
            for l2 in maplines:
                if mergeone is True: break
                if l1 != l2:
                    if l1.front == l2.front:
                        if l1.back == l2.back:
                            if l1.angle == l2.angle:
                                if MapLine.share_a_point(l1,l2):
                                    # if all the data lines up...
                                    new = MapLine.merged_line(l1,l2)
                                    if new is not None:
                                        # and we successfully created a new linedef...
                                        maplines.append(new) # add the new linedef
                                        l1.remain = False # remove the old ones that got merged
                                        l2.remain = False
                                        maplines[:] = [x for x in maplines if not x.remain is False]
                                        mergeone = True
                                        break # and go from the start!
    print "map lines at end: {}".format(len(maplines))
    return maplines

# get a sidedef, create it if it doesn't exist already
def get_sidedef(omap, tx_up, tx_low, tx_mid, sector):
    for s in omap.sidedefs:
        if s.tx_up == tx_up and s.tx_low == tx_low and s.tx_mid == tx_mid and s.sector == sector:
            return omap.sidedefs.index(s)
    ns = omg.mapedit.Sidedef(tx_up = tx_up, tx_low = tx_low, tx_mid = tx_mid, sector = sector)
    omap.sidedefs.append(ns)
    return len(omap.sidedefs) - 1

# get a vertex, create it if it doesn't exist already
def get_vertex(omap, x, y):
    for v in omap.vertexes:
        if v.x == x and v.y == y:
            return omap.vertexes.index(v)
    nv = omg.mapedit.Vertex(x=x,y=y)
    omap.vertexes.append(nv)
    return len(omap.vertexes) - 1

# convert linedata to doom format map, and output the wad
def linedata2doom(lines, mapsectors, void):
    owad = omg.WAD()
    omap = omg.mapedit.MapEditor()

    for s in mapsectors:
        omap.sectors.append(s.get_sector())
        omap.sidedefs.append(s.get_sidedef())
        omap.sidedefs[len(omap.sidedefs)-1].sector = len(omap.sectors)-1

    for m in lines:
        if m.remain:
            omap.linedefs.append(omg.mapedit.Linedef(vx_a = get_vertex(omap,m.x1,m.y1),
                                                     vx_b = get_vertex(omap,m.x2,m.y2),
                                                     front = m.front-1,
                                                     back = m.back-1))

    # fix sidedef textures for two-sided lines
    for ld in omap.linedefs:
        if ld.back != -1:
            # get textures from back sidedef
            bsd = omap.sidedefs[ld.back]
            fsd = omap.sidedefs[ld.front]
            ld.back = get_sidedef(omap, fsd.tx_mid, fsd.tx_mid, '-', bsd.sector)
            ld.front = get_sidedef(omap, bsd.tx_mid, bsd.tx_mid, '-', fsd.sector)

    owad.maps["MAP01"] = omap.to_lumps()
    return owad

# convert an image all the way to a doom map, fun!
def image2tiles2lines2doom(image, mapsectors, void):
    print "image to tiles" 
    tiles = image_to_tiles(image)
    print "tiles 2 linedata"
    lines = tiles2linedata(tiles, void)
    print "linedata 2 doom"
    output = linedata2doom(lines, mapsectors, void)
    return output

# convert tiles to a doom map
def tile2doom(tiles, mapsectors, void):
    print "converting tiles to map"
    owad = omg.WAD()
    omap = omg.mapedit.MapEditor()

    player_placed = 0

    for i in range(len(tiles)):
        print "tile {}/{}".format(i+1,len(tiles))
        for j in range(len(tiles[i])):
            if tiles[i][j] != void:
                ms = mapsectors[tiles[i][j] - 1]
                if player_placed == 0:
                    player_placed = 1
                    omap.things.append(omg.mapedit.Thing(x=(i*TILESIZE)+(TILESIZE/2),y=(j*TILESIZE)+(TILESIZE/2),type=1))
                verts = []
                verts.append((i * TILESIZE, j * TILESIZE))
                verts.append(((i+1) * TILESIZE, j * TILESIZE))
                verts.append(((i+1) * TILESIZE, (j+1) * TILESIZE))
                verts.append((i * TILESIZE, (j+1) * TILESIZE))
                omap.draw_sector(verts,sector=ms.get_sector(),sidedef=ms.get_sidedef())

    owad.maps["MAP01"] = omap.to_lumps()

    return owad

# convert coords format to 2darray. TODO: just load coords format directly
def coords22darray(coords,width,height, void):
    tiles = [[void for y in range(width)] for x in range(height)]
    for c in coords:
        tiles[c[0]][c[1]] = c[2]
    return tiles

# convert the "sectors" portion of a json data file into a MapSectors array
def load_json_sectors(json_sectors):
    output = []
    for s in json_sectors:
        output.append(MapSector(s["texture"],s["floor"],s["ceil"],s["z_floor"],s["z_ceil"]))
    return output

# convert a json data file all the way into a doom map!
def json2doom(data):
    if data["version"] != "0.1": 
        print "Sorry, invalid version in json: {}".format(data["version"])
        return None

    global TILESIZE
    TILESIZE = data["tilesize"]
    # to lines

    # 2darray vs coords:
    # 2darray is a big ol' square of tile indexes, v simple to read and
    # more compact when a lot of the area inside the bounds of the map is filled
    # coords is a list of position,index values which define where each tile is an
    # d what it is. this is more compact when the bounds of the map has a much
    # bigger area than the map coverage itself.
    # at a guess i'd say if more than 1/4 of the bounds area is covered, then 
    # 2darray is smaller. we'll just have to see what it's like in practice.
    # the reasoning is, 2darray has to define every void tile inbetween and around 
    # the existing tiles, yet coords only defines the tiles that exist. however,
    # the coords data is much larger than the 2darray data. while 2darray only needs
    # on average 2 characters (but often only 1) to define the tile, coords needs
    # around 10~11. it's up to the editing application to decide which will be 
    # better to save as. I'd recommend creating both and checking the size but
    # that might be overkill. maybe it's possible to calculate easy enough

    if data["format"] == "2darray": 
        lines = tiles2linedata(data["tiles"],data["void"])

    if data["format"] == "coords":
        width = data["width"]
        height = data["height"]
        tiles = coords22darray(data["tiles"],data["width"],data["height"],data["void"])
        lines = tiles2linedata(tiles, data["void"])

    output = linedata2doom(lines, load_json_sectors(data["sectors"]), data["void"])
    return output

# test stuff
if __name__=="__main__":
    with open("testlevel.json") as jfile:
        owad = json2doom(json.load(jfile))
    owad.to_file("test.wad")
