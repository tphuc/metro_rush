import pyglet
from pyglet.window import key, mouse
from parseline import *
from random import randint
from math_helper import *

frame_rate = 1/60
time_wait = 2.0
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
           'orange': rsc_path+'orangedot'+prefix,
           'white': rsc_path+'whitedot'+prefix}
colors = ['red','blue','green','yellow','pink','violet','magenta','orange']
train_img = 'dot/train_img.png'
WIDTH = 1000
HEIGHT = 800
mainbatch = pyglet.graphics.Batch()
runtime_file = 'runtime_data'
location_file = 'stations.csv'

background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)


class KEY:
    zoomin = key.Z
    zoomout = key.X
    up = key.W
    down = key.S
    left = key.A
    right = key.D
    drag = key.G
    outputfile = key.ENTER
    ctrl = 18
    shift = 17


class MODE:
    free = 0
    select = 1
    draging = 2


class SelectRect:
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0
    display = False


class RailGrid:
    col = 0
    row = 0


Cardinal = {'NS': (0, -1),
            'SN': (0,  1),
            'EW': (-1, 0),
            'WE': (1,  0)}


def drawline(start_x, start_y, end_x, end_y):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                         ("v2f", (start_x, start_y, end_x, end_y)),
                         ('c3B', (150, 150, 150, 150, 150, 150)))


def draw_rectangle(start_x, start_y, end_x, end_y):
    pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP, ('v2f', [
                         start_x, start_y, end_x, start_y, end_x, end_y, start_x, end_y]))


class Station(pyglet.sprite.Sprite):
    size = 5

    def __init__(self, name, colorSprite, x, y, colorgroup, intersect=False):
        self.texture = pyglet.image.load(colorSprite)
        self.texture.anchor_x = self.texture.width // 2
        self.texture.anchor_y = self.texture.height // 2
        self.intersect = intersect
        self.rail_color = colorgroup
        super(Station, self).__init__(self.texture,
                                      x=x, y=y, batch=mainbatch, group=background)
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

    def drag(self, dx, dy):
        self.x += dx
        self.y += dy

    def create_label(self):
        self.label = pyglet.text.Label(text=self.name, x=self.x, y=self.y+self.height,
                                       anchor_x='center', anchor_y='bottom', batch=mainbatch, group=foreground)

    def delete_label(self):
        if self.label:
            self.label.delete()
            self.label = None

    def is_hovering(self, x, y):
        if self.x+self.width//2 > x > self.x-self.width//2 and \
                self.y+self.height//2 > y > self.y-self.height//2:
            if not self.label:
                self.create_label()
            return True
        else:
            self.delete_label()
            return False

    def is_select(self, start_x, start_y, end_x, end_y):
        return end_x > self.x > start_x and start_y > self.y > end_y


class RailWay:
    disparity = (-5, 5)
    intersect = []

    def __init__(self, direction, ntrains, names, start_x=0, start_y=0, color=None, locations=[], group='Untilted'):
        self.ntrains = ntrains
        self.names = names
        self.locations = locations
        self.color = color
        self.group = group
        self.start_x, self.start_y = start_x, start_y
        self.sprite_img = self.get_sprite_img(color)
        self.direction = direction
        self.interval = 40
        self._init_stations()

    def get_sprite_img(self, color):
        return CSprite[color]

    def _init_stations(self):
        self.stations = []
        for i in range(self.ntrains):
            if not self.locations:
                x = self.start_x + \
                    self.direction[0]*i*self.interval + \
                    self.direction[1]*randint(*RailWay.disparity)
                y = self.start_y + \
                    self.direction[1]*i*self.interval + \
                    self.direction[0]*randint(*RailWay.disparity)
            else:
                x = self.locations[i][0]
                y = self.locations[i][1]

            if self.names[i].find("Conn") != -1:
                name = self.names[i][:self.names[i].find(':')]
                if name not in [s.name for s in RailWay.intersect]:
                    station = Station(
                        name, CSprite['white'], x, y, 'white', intersect=True)
                    self.stations.append(station)
                    RailWay.intersect.append(station)
                else:
                    for station in RailWay.intersect:
                        if station.name == name:
                            self.stations.append(station)
            else:
                self.stations.append(
                    Station(self.names[i], self.sprite_img, x, y, self.color))

    def _draw_lines(self):
        for i in range(len(self.stations)-1):
            drawline(self.stations[i].x, self.stations[i].y,
                     self.stations[i+1].x, self.stations[i+1].y)

    def drawline(self):
        self._draw_lines()

    def scale(self, scale):
        for station in self.stations:
            station.scale(scale)


class Train(pyglet.sprite.Sprite):
    size = 10
    dcheck = 2

    def __init__(self, _id, start_station):
        self.texture = pyglet.image.load('dot/train_img.png')
        self.texture.anchor_x = self.texture.width // 2
        self.texture.anchor_y = self.texture.height // 2
        """ path: list of station object """
        self.current_station = start_station
        x = self.current_station.x
        y = self.current_station.y
        super(Train, self).__init__(self.texture, x=x,
                                    y=y, batch=mainbatch, group=foreground)
        self.path = [self.current_station]
        self.id = _id
        self.velx, self.vely = 0, 0
        self.rot = 0
        self.finish_turn = False
        self._setup()

    def _setup(self):
        self.scalex = Train.size / self.width
        self.scaley = Train.size / self.height
        self.update(scale_x=self.scalex, scale_y=self.scaley)

    def scale(self, scale_):
        self.scalex *= scale_
        self.scaley *= scale_
        self.update(scale_x=self.scalex, scale_y=self.scaley)

    def set_vel(self, dx, dy):
        """ move every frame dx dy """
        self.velx = dx
        self.vely = dy

    def stop(self):
        """ can be called as set_vel(0,0) """
        self.set_vel(0, 0)

    def move(self):
        self.x += self.velx
        self.y += self.vely

    def set_rot(self, angles):
        self.rotation = angles*-1

    def doupdate(self, target):
        direction = direction_vec(self, target)
        self.set_vel(direction[0], direction[1])
        rot = get_vector_rot(direction)
        self.set_rot(rot)

    def _move_to(self, dt):
        target = self.path[0]
        if target.x-Train.dcheck <= self.x <= target.x+Train.dcheck and \
                target.y-Train.dcheck <= self.y <= target.y+Train.dcheck:
            self.finish_turn = True
            self.path.remove(target)
            pyglet.clock.unschedule(self._move_to)
            self.stop()

        else:
            self.doupdate(target)

    def move_to_next_station(self):
        pyglet.clock.schedule(self._move_to)


class Controller:
    def __init__(self, trains, stations, data):
        self.trains = trains
        self.stations = stations
        self.setup_metro_traffic(data)

    def setup_metro_traffic(self, data):
        step_commands = data.split('\n')
        for commands in step_commands:
            commands = commands.split('|')
            for command in commands:
                labels = command[command.rfind('-')+1:]
                station_name = command[:command.find('(')]
                trains = self._get_trains_by_labels(labels)
                station = self.get_station_by_name(station_name)
                for train in trains:
                    train.path.append(station)

    def tick(self, dt):
        for train in self.trains:
            train.move()

    def runstep(self, dt):
        all_finish_turn = self.is_end_turn()
        if all_finish_turn:
            for train in self.trains:
                train.finish_turn = False

        for train in self.trains:
            if len(train.path):
                if not train.finish_turn:
                    train.move_to_next_station()

    def is_end_turn(self):
        for train in self.trains:
            if train.finish_turn == False:
                return False
        return True

    def get_station_by_name(self, name):
        for station in self.stations:
            if station.name == name:
                return station

    def _get_trains_by_labels(self, labels):
        ids = [int(label[1:]) for label in labels.split(',')]
        trains = []
        for id in ids:
            trains.append(self.trains[id-1])
        return trains
