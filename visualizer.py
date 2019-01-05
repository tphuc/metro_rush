
from _visualizer import *


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
        ############### mode ################
        """ window modes:
        - moving = 0
        - selecting = 1
        - dragging = 2
        """
        self.mode = MODE.free
        self.selecting = None
        """ Label display name:
        - display station name when mouse hovering on
        """
        ####################################################################################################
        """ store all the railways """
        self.railways = []
        self.stations = []
        self.init_transit_map()
        

    def init_transit_map(self):
        self.railways.append(RailWay('horizontal', len(self.station_dict['Red Line']), self.station_dict['Red Line'],
                                     50, 400, 'red'))
        self.railways.append(RailWay('horizontal', len(self.station_dict['Violet Line']), self.station_dict['Violet Line'],
                                     50, 300, 'magenta'))
        for railway in self.railways:
            self.stations += [station for station in railway.stations if station not in self.stations]

    def screen_up(self):
        self.focusY -= self.moverate
        self.doupdate()

    def screen_down(self):
        self.focusY += self.moverate
        self.doupdate()

    def screen_left(self):
        self.focusX += self.moverate
        self.doupdate()

    def screen_right(self):
        self.focusX -= self.moverate
        self.doupdate()

    def screen_zoomin(self):
        self.scaleX *= self.zoominrate
        self.scaleY *= self.zoominrate
        self.doupdate()

    def screen_zoomout(self):
        self.scaleX *= self.zoomoutrate
        self.scaleY *= self.zoomoutrate
        self.doupdate()

    def doupdate(self):
        for station in self.stations:
            station.x *= self.scaleX
            station.y *= self.scaleY
            station.scale(self.scaleX)

        self.scaleX, self.scaleY = 1, 1

        centerx = sum([sum([s.x for s in railway.stations]) //
                       railway.ntrains for railway in self.railways]) // len(self.railways)
        centery = sum([sum([s.y for s in railway.stations]) //
                       railway.ntrains for railway in self.railways]) // len(self.railways)

        for station in self.stations:
            station.x += self.focusX - centerx
            station.y += self.focusY - centery

    def reset_mode(self):
        self.mode = MODE.free

    ############################ window events ################################
    """
    @window.event
    Below is a list of event handler from window
    """

    def on_draw(self):
        self.clear()
        for railway in self.railways:
            railway.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == KEY.up:
            self.screen_up()
            self.reset_mode()
        elif symbol == KEY.right:
            self.screen_right()
            self.reset_mode()
        elif symbol == KEY.down:
            self.screen_down()
            self.reset_mode()
        elif symbol == KEY.left:
            self.screen_left()
            self.reset_mode()
        elif symbol == KEY.zoomin:
            self.screen_zoomin()
            self.reset_mode()
        elif symbol == KEY.zoomout:
            self.screen_zoomout()
            self.reset_mode()
        elif symbol == KEY.drag:
            self.mode = MODE.draging
        else:
            self.reset_mode()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.selecting:
            self.selecting.setxy(x, y)
            self.selecting.delete_label()

    def on_mouse_press(self, x, y, button, modifiers):
        self.selecting = None
        for railway in self.railways:
            for station in railway.stations:
                if station.is_hovering(x, y):
                    self.selecting = station
                    return

    def on_mouse_release(self, x, y, button, modifiers):
        self.selecting = None

    def on_mouse_motion(self, x, y, dx, dy):
        for railway in self.railways:
            for station in railway.stations:
                station.is_hovering(x, y)


if __name__ == "__main__":
    window = Window(WIDTH, HEIGHT)
    window.doupdate()
    pyglet.app.run()
