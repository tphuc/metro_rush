
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

        #self.station_dict = parseLineStations('delhi-metro-stations')
        ############### mode ################
        """ window modes:
        - moving = 0
        - selecting = 1
        - dragging = 2
        """
        self.mode = MODE.free
        self.selecting = []
        """ Label display name:
        - display station name when mouse hovering on
        """
        ####################################################################################################
        """ store all the railways """
        self.railways = []
        self.stations = []
        self.cols = 6
        self.rows = 6
        #self.init_transit_map()
    
    def setup_grid(self, ncol, nrow):
        self.cols = ncol
        self.rows = nrow


    def addRail(self, direction, names, color):
        dir_vector = Cardinal[direction]
        if direction.find("N") != -1:
            RailGrid.col += 1
            if dir_vector[1] == 1:
                startloc = self.width * RailGrid.col/self.cols, 0
            else:
                startloc = self.width * RailGrid.col/self.cols, self.height
        else:
            RailGrid.row += 1
            if dir_vector[0] == 1:
                startloc = 0, self.height*(1-RailGrid.row/self.rows)
            else:
                startloc = self.width, self.height*(1-RailGrid.row/self.rows)
            print(startloc, str(dir_vector))
        self.railways.append(RailWay(dir_vector, len(names), names , *startloc, color))
        for railway in self.railways:
            self.stations += [station for station in railway.stations if station not in self.stations]

    def init_transit_map(self):
        self.station_dict = parseLineStations('delhi-metro-stations')
        self.railways.append(RailWay((0, -1), len(self.station_dict['Red Line']), self.station_dict['Red Line'],
                                     50, 800, 'red'))
        self.railways.append(RailWay((0, 1), len(self.station_dict['Violet Line']), self.station_dict['Violet Line'],
                                     500, 0, 'pink'))
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
        if SelectRect.display:
            draw_rectangle(SelectRect.start_x, SelectRect.start_y, SelectRect.end_x, SelectRect.end_y)

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
        elif symbol == KEY.outputfile:
            self.outputfile()
        else:
            self.reset_mode()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.selecting:
            for selected in self.selecting:
                if buttons & KEY.drag:
                    selected.drag(dx, dy)
                else:
                    selected.setxy(x, y)
                selected.delete_label()
        else:
            SelectRect.end_x = x + dx
            SelectRect.end_y = y + dy
            SelectRect.display = True

    """ fired once event : mouse click"""
    def on_mouse_press(self, x, y, button, modifiers):
        SelectRect.start_x = x
        SelectRect.start_y = y
        if not self.selecting:
            for station in self.stations:
                if station.is_hovering(x, y):
                    if modifiers in [key.MOD_CTRL, key.MOD_SHIFT] and station.rail_color != 'white':
                        for station in self.stations:
                            if station.is_hovering(x, y):
                                for railway in self.railways:
                                    if railway.color == station.rail_color:
                                        if modifiers == key.MOD_CTRL:
                                            self.selecting = [station for station in railway.stations if station.rail_color != 'white']
                                        else:
                                            self.selecting = railway.stations
                                        return

                    else:
                        self.selecting.append(station)
                    return

    """ fired once event """
    def on_mouse_release(self, x, y, button, modifiers):
        SelectRect.display = False
        if not self.selecting:
            for station in self.stations:
                if station.is_select(SelectRect.start_x, SelectRect.start_y, SelectRect.end_x, SelectRect.end_y):
                    self.selecting.append(station)
            SelectRect.start_x = 0
        else:
            self.selecting = []

    def on_mouse_motion(self, x, y, dx, dy):
        for station in self.stations:
            station.is_hovering(x, y)

    def reset_select(self):
        SelectRect.start_x = 0
        SelectRect.start_y = 0
        SelectRect.end_x = 0
        SelectRect.end_y = 0

    def outputfile(self):
        data = ""
        for railway in self.railways:
            data += "#" + railway.color + '\n'
            for station in railway.stations:
                data += "{}, {}, {}\n".format(station.name, str(int(station.x)), str(int(station.y)))
        with open('stations', 'w+') as f:
            f.write(data)

if __name__ == "__main__":
    window = Window(WIDTH, HEIGHT)
    station_dict = parseLineStations('delhi-metro-stations')
    window.addRail('EW', station_dict['Red Line'], 'red')
    window.addRail('NS', station_dict['Yellow Line'], 'yellow')
    # window.addRail('WE', station_dict['Blue Line'], 'blue')
    # window.addRail('SN', station_dict['Magenta Line'], 'magenta')
    # window.addRail('NS', station_dict['Pink Line'], 'pink')
    # window.addRail('NS', station_dict['Violet Line'], 'violet')
    # window.addRail('NS', station_dict['Airport Express'], 'orange')
    # window.init_transit_map()
    window.doupdate()
    pyglet.app.run()
