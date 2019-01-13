
from _visualizer import *
from random import randint

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
        ####################################################################################################
        """ store the state of the network """
        self.start_station = None
        self.end_station = None
        self.ntrains = 0
        self.trains = []

    def setup_grid(self, ncol, nrow):
        self.cols = ncol
        self.rows = nrow


    def addRail(self, direction, names, color, group, locations=[]):
        """ automatic generate if not specified locations """
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

        """ create Railway object """
        if not locations:
            self.railways.append(RailWay(dir_vector, len(names), names , startloc[0], startloc[1], color=color, group=group))
        else:
            self.railways.append(RailWay(dir_vector, len(names), names,  color=color, locations=locations, group=group))

        for railway in self.railways:
            self.stations += [station for station in railway.stations if station not in self.stations]

    def init_transit_map(self, station_dict):
        def is_valid_color(color):
            return color in colors
        for group, line in station_dict.items():
            color = group[:group.find(' ')].lower()
            dir = list(Cardinal.keys())[randint(0,3)]
            if is_valid_color(color):
                self.addRail(dir, line, group=group, color=color)
            else:
                self.addRail(dir, line, group=group, color='orange')

    def set_start_end(self, start_line, start_id, end_line, end_id):
        """ set the route for the network """
        for railway in self.railways:
            if railway.color == start_line:
                self.start_station = railway[start_id-1]
            if railway.color == end_line:
                self.end_station = railway[end_id-1]

    def set_ntrains(self, n):
        self.ntrains = n


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
            station.x = (station.x - self.width/2)*self.scaleX + self.focusX
            station.y = (station.y - self.height/2)*self.scaleY + self.focusY
            station.scale(self.scaleX)
        for train in self.trains:
            train.x = (train.x - self.width/2)*self.scaleX + self.focusX
            train.y = (train.y - self.height/2)*self.scaleY + self.focusY
            train.scale(self.scaleX)

        #Reset all
        self.scaleX, self.scaleY = 1, 1
        self.focusX = self.width//2
        self.focusY = self.height//2

    ############################ window events ################################
    """
    @window.event
    Below is a list of event handler from window
    """

    def on_draw(self):
        self.clear()
        mainbatch.draw()

        for railway in self.railways:
            railway.drawline()
        if SelectRect.display:
            draw_rectangle(SelectRect.start_x, SelectRect.start_y, SelectRect.end_x, SelectRect.end_y)

    def on_key_press(self, symbol, modifiers):
        if symbol == KEY.up:
            self.screen_up()
        elif symbol == KEY.right:
            self.screen_right()
        elif symbol == KEY.down:
            self.screen_down()
        elif symbol == KEY.left:
            self.screen_left()
        elif symbol == KEY.zoomin:
            self.screen_zoomin()
        elif symbol == KEY.zoomout:
            self.screen_zoomout()
        elif symbol == KEY.drag:
            self.mode = MODE.draging
        elif symbol == KEY.outputfile:
            self.outputfile()


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
        def select_multiple():
            for railway in self.railways:
                if railway.color == station.rail_color:
                    if modifiers == KEY.ctrl:
                        self.selecting = [station for station in railway.stations if station.rail_color != 'white']
                    else:
                        self.selecting = railway.stations
                    return

        SelectRect.start_x = x
        SelectRect.start_y = y

        if not self.selecting:
            for station in self.stations:
                if station.is_hovering(x, y):
                    if modifiers in [KEY.ctrl, KEY.shift] and station.rail_color != 'white':
                        select_multiple()
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
        with open(location_file, 'w+') as f:
            f.write(data)

    def configurate(self, attrs, ntrains):
        for railway in self.railways:
            if railway.group == attrs['START'][0] and not self.start_station:
                self.start_station = railway.stations[int(attrs['START'][1])-1]
            if railway.group == attrs['END'][0] and not self.end_station:
                self.end_station = railway.stations[int(attrs['END'][1])-1]
        self.ntrains = ntrains

    def stimulate(self, data):
        for i in range(self.ntrains):
            self.trains.append(Train(i+1, self.start_station))
        controller = Controller(self.trains, self.stations, data)
        pyglet.clock.schedule(controller.tick)
        pyglet.clock.schedule_interval(controller.runstep, time_wait)

    def print_status(self):
        print(self.start_station, self.end_station)
        print("n stations:",len(self.stations), "/ n railways: ", len(self.railways))


def run(file, automatic=False):
    window = Window(WIDTH, HEIGHT)
    station_dict, attrs, ntrains = parseLineStations(file)
    if not automatic:
        location_dict = parseLocationStations(location_file)
        window.addRail('EW', station_dict['Red Line'], group='Red Line', color='red', locations=location_dict['Red Line'])
        window.addRail('NS', station_dict['Yellow Line'],group='Yellow Line', color='yellow', locations=location_dict['Yellow Line'])
        window.addRail('WE', station_dict['Blue Line'], group='Blue Line', color='blue', locations=location_dict['Blue Line'])
        window.addRail('SN', station_dict['Magenta Line'],group='Magenta Line', color='magenta', locations=location_dict['Magenta Line'])
        window.addRail('NS', station_dict['Pink Line'], group='Pink Line', color='pink', locations=location_dict['Pink Line'])
        window.addRail('NS', station_dict['Violet Line'], group = 'Violet Line', color='violet', locations=location_dict['Violet Line'])
        window.addRail('NS', station_dict['Airport Express'], group = 'Airport Express', color='orange', locations=location_dict['Airport Express'])
    else:
        window.init_transit_map(station_dict)
    window.configurate(attrs, ntrains)
    data_run = open(runtime_file,'r').read().strip()
    window.stimulate(data_run)
    pyglet.app.run()

if __name__ == '__main__':
    run('delhi-metro-stations')
