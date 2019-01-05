import pyglet
from pyglet.window import key, mouse
from parseline import parseLineStations
from random import randint

# http://www.poketcode.com/en/pyglet/index.html
rsc_path = 'dot/'
prefix = '.png'
CSprite = {'red': rsc_path+'reddot'+prefix,
           'blue': rsc_path+'bluedot'+prefix,
           'green': rsc_path+'greendot'+prefix,
           'yellow': rsc_path+'yellowdot'+prefix,
           'pink': rsc_path + 'pinkdot'+prefix,
           'violet': rsc_path+'violetdot'+prefix,
           'magenta': rsc_path+'magentadot'+prefix,
           'brown': rsc_path+'browndot'+prefix,
           'white': rsc_path+'whitedot'+prefix}

WIDTH = 1000
HEIGHT = 800
batch = pyglet.graphics.Batch()

background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)


class MARGIN:
    up = 30
    left = WIDTH*7/8


class BODY:
    top1 = HEIGHT//16
    top2 = top1 + MARGIN.up
    top3 = top1 + MARGIN.up*2
    top4 = top1 + MARGIN.up*3
    top5 = top1 + MARGIN.up*4
    top6 = top1 + MARGIN.up*6
    middle = HEIGHT//2
    bottom1 = HEIGHT * 6/8
    bottom2 = HEIGHT * 7/8
    buttonwidth = 15
    dropdownwidth = 12


class KEY:
    zoomin = key.Z
    zoomout = key.X
    up = key.W
    down = key.S
    left = key.A
    right = key.D
    drag = key.G


class MODE:
    free = 0
    select = 1
    draging = 2


def drawline(start_x, start_y, end_x, end_y):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                         ("v2f", (start_x, start_y, end_x, end_y)))

def set_line_width(width):
    pyglet.gl.glLineWidth(width)


class Station(pyglet.sprite.Sprite):
    size = 10

    def __init__(self, name, colorSprite, x, y, intersect=False):
        self.texture = pyglet.image.load(colorSprite)
        self.texture.anchor_x = self.texture.width // 2
        self.texture.anchor_y = self.texture.height // 2
        super(Station, self).__init__(self.texture,
                                      x=x, y=y, batch=batch, group=background)
        self.name = name
        self.label = None
        self._setup()

    def _setup(self):
        self.scalex = Station.size / self.width
        self.scaley = Station.size / self.height
        self.update(scale_x=self.scalex, scale_y=self.scaley)

    def offset(self, x, y):
        self.x += x
        self.y += y

    def scale(self, scale_):
        self.scalex *= scale_
        self.scaley *= scale_
        self.update(scale_x=self.scalex, scale_y=self.scaley)

    def setxy(self, x, y):
        self.x = x
        self.y = y
        self.display_label = False

    def drag(self, x, y, dx, dy):
        self.x += dx*1.1
        self.y += dy*1.1

    def create_label(self):
        self.label = pyglet.text.Label(text=self.name, x=self.x, y=self.y+self.height,
                                       anchor_x='center', anchor_y='bottom', batch=batch, group=foreground)

    def delete_label(self):
        if self.label:
            self.label.delete()
            self.label = None

    def is_hovering(self, x, y):
        if self.x+self.width//2 > x > self.x - self.width//2 and self.y + self.height//2 > y > self.y - self.height//2:
            if not self.label:
                self.create_label()
            return True
        else:
            self.delete_label()
            return False


class RailWay:
    disparity = (-5, 5)
    intersect = []

    def __init__(self, direction, ntrains, names, start_x, start_y, color):
        self.ntrains = ntrains
        self.names = names
        self.start_x, self.start_y = start_x, start_y
        self.sprite_img = self.get_sprite_img(color)
        self.direction = self.get_line_direction(direction)
        self._init_stations()

    def get_sprite_img(self, color):
        return CSprite[color]

    def get_line_direction(self, direction):
        self.interval = 40
        return 1, 0
        # if direction == 'horizontal':
        #     self.interval = WIDTH / self.ntrains - self.ntrains
        #     return (1, 0)
        # elif direction == 'vertical':
        #     self.interval = HEIGHT / self.ntrains - self.ntrains
        #     return (0, -1)

    def _init_stations(self):
        self.stations = []
        for i in range(self.ntrains):
            x = self.start_x + \
                self.direction[0]*i*self.interval + \
                self.direction[1]*randint(*RailWay.disparity)
            y = self.start_y + \
                self.direction[1]*i*self.interval + \
                self.direction[0]*randint(*RailWay.disparity)

            if self.names[i].find("Line") > 0:
                name = self.names[i][:self.names[i].find(':')]
                if name not in [s.name for s in RailWay.intersect]:
                    station = Station(name, CSprite['white'], x, y)
                    self.stations.append(station)
                    RailWay.intersect.append(station)
                else:
                    for station in RailWay.intersect:
                        if station.name == name:
                            self.stations.append(station)
            else:
                self.stations.append(
                    Station(self.names[i], self.sprite_img, x, y))

    def draw_lines(self):
        for i in range(len(self.stations)-1):
            drawline(self.stations[i].x, self.stations[i].y,
                     self.stations[i+1].x, self.stations[i+1].y)

    def draw(self):
        batch.draw()
        self.draw_lines()

    def offset(self, y, x):
        pass

    def scale(self, scale):
        for station in self.stations:
            station.scale(scale)

    def doupdate(self, scale):
        for station in self.stations:
            station.doupdate()