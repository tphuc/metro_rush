import pyglet
from random import randint
class Circle(pyglet.sprite.Sprite):
    def __init__(self, radiance=5, x=0, y=0):
        self.texture = pyglet.image.load('dot/reddot.png')
        super(Circle, self).__init__(self.texture, x=x, y=y)
        self.update(scale=0.2)

    def click(self, x, y):
        if x >= self.x and y >= self.y:
            if x <= self.x + self.width and y <= self.y + self.height:
                return self

mouse = pyglet.window.mouse

#VARS
window = pyglet.window.Window(width = 800, height = 600)
score = 0
#circleImg = pyglet.image.load("circle.png")
#circle = pyglet.sprite.Sprite(circleImg, randint(1, window.width), randint(1, window.height))
circle1 = Circle(x=50, y=50)
circle2 = Circle(x=200,y=200)
circles = []
circles.append(circle1)
circles.append(circle2)
text = pyglet.text.Label("Click red!", font_name = "Times New Roman", font_size = 18, x = 260, y = 10)


#DETECT MOUSE PRESS ON CIRCLE
@window.event
def on_mouse_press(x, y, button, modifiers):
    for circle in circles:
        if circle.click(x, y):
            print('Clicked in circle')
            circle.x = randint(0, window.width - 10)
            circle.y = randint(0, window.height - 10)

@window.event
def on_draw():
    window.clear()
    text.draw()
    for circle in circles:
        circle.draw()

pyglet.app.run()