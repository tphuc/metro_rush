import pyglet
from pyglet.window import key
from parseline import parseLineStations
from random import randint
#http://www.poketcode.com/en/pyglet/index.html
rsc_path = 'dot/'
prefix = '.png'
CSprite = {'red':rsc_path+'reddot'+prefix,
           'blue': rsc_path+'bluedot'+prefix,
           'green' : rsc_path+'greendot'+prefix,
           'yellow' : rsc_path+'yellowdot'+prefix,
           'pink' : rsc_path +'pinkdot'+prefix,
           'violet': rsc_path+'violetdot'+prefix,
           'magenta': rsc_path+'magentadot'+prefix,
           'brown': rsc_path+'browndot'+prefix}

WIDTH = 1000
HEIGHT = 800



class KEY:
    zoomin = key.Z
    zoomout = key.X
    up = key.W
    down = key.S
    left = key.A
    right = key.D

class Station:
    size = 10
    def __init__(self, name, colorSprite, x, y, intersect=False):
        self.x, self.y = x, y
        self._create_sprite(colorSprite, self.x, self.y)
        
    def _create_sprite(self, colorSprite, x, y):
        self.image = pyglet.image.load(colorSprite)
        self.sprite = pyglet.sprite.Sprite(self.image, x, y)
        self.scalex = Station.size / self.sprite.width
        self.scaley = Station.size / self.sprite.height
        self.sprite.update(scale_x = self.scalex, scale_y=self.scaley)
    
    def draw(self):
        self.sprite.draw()

    def offset(self, x, y):
        self.sprite.x += x
        self.sprite.y += y
    
    def scale(self, scale_):
        self.scalex *= scale_
        self.scaley *= scale_
        self.sprite.update(scale_x=self.scalex, scale_y=self.scaley)
    
    def doupdate(self):
        pass

class RailWay():
    disparity = (-10,10)


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
        if direction == 'horizontal':
            self.interval = WIDTH / self.ntrains - self.ntrains
            return (1, 0)
        if direction == 'vertical':
            self.interval = HEIGHT / self.ntrains - self.ntrains
            return (0, -1)
    
    def _init_stations(self):
        self.stations = []
        for i in range(self.ntrains):
            x = self.start_x + self.direction[0]*i*self.interval + self.direction[1]*randint(*RailWay.disparity)
            y = self.start_y + self.direction[1]*i*self.interval + self.direction[0]*randint(*RailWay.disparity)
            self.stations.append(Station(self.names[i], self.sprite_img, x, y))

    def draw(self):
        for station in self.stations:
            station.draw()

    def offset(self, y, x):
        pass
    
    def scale(self, scale):
        for station in self.stations:
            station.scale(scale)
    
    def doupdate(self, scale):
        for station in self.stations:
            station.doupdate()







    


class Window(pyglet.window.Window):
    def __init__(self, width, height):
        super(Window, self).__init__(width=width, height=height)
        self.width = width
        self.height = height
        self.scaleX = 1
        self.scaleY = 1
        self.focusX = self.width//2
        self.focusY = self.height//2
        self.zoominrate = 1.3
        self.zoomoutrate = 0.8
        self.moverate = 50
        self.station_dict = parseLineStations('delhi-metro-stations')
        self.railwayred = RailWay('horizontal', len(self.station_dict['Red Line']), self.station_dict['Red Line'],
                     50, 400, 'red')

    def screen_up(self):
        self.focusY += self.moverate

    def screen_down(self):
        self.focusY -= self.moverate

    def screen_left(self):
        self.focusX += self.moverate

    def screen_right(self):
        self.focusX -= self.moverate

    def screen_zoomin(self):
        self.scaleX *= self.zoominrate
        self.scaleY *= self.zoominrate
        self.doupdate()

    def screen_zoomout(self):
        self.scaleX *= self.zoomoutrate
        self.scaleY *= self.zoomoutrate
        self.doupdate()

    def doupdate(self):
        for station in self.railwayred.stations:
            station.sprite.x *= self.scaleX
            station.sprite.y *= self.scaleY
            station.scale(self.scaleX)
        self.scaleX, self.scaleY = 1, 1
        centerx = sum([s.sprite.x for s in self.railwayred.stations], 0) // self.railwayred.ntrains
        centery = sum([s.sprite.y for s in self.railwayred.stations], 0) // self.railwayred.ntrains
        for station in self.railwayred.stations:
            station.sprite.x += self.focusX - centerx
            station.sprite.y += self.focusY - centery


    def on_draw(self):
        self.clear()
        self.railwayred.draw()


    def on_key_press(self, symbol, modifiers):
        if symbol == KEY.up:
            self.screen_up()
        elif symbol == KEY.right:
            self.screen_right()
        elif symbol == KEY.down:
            self.screen_down()
        elif symbol == KEY.right:
            self.screen_left()
        elif symbol == KEY.zoomin:
            self.screen_zoomin()
        elif symbol == KEY.zoomout:
            self.screen_zoomout()

window = Window(800, 600)
window.doupdate()
pyglet.app.run()