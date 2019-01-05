import pyglet

window = pyglet.window.Window()
class SelectRect:
    start_x = 100
    start_y = 100
    end_x = 200
    end_y = 200
    display = True

def draw_rectangle(start_x, start_y, end_x, end_y):
    pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP, ('v2f', [start_x, start_y, end_x, start_y, end_x, end_y, start_x, end_y ]))

@window.event
def on_mouse_press(x, y, button, modifiers):
    SelectRect.start_x = x
    SelectRect.start_y = y

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    SelectRect.end_x = x + dx
    SelectRect.end_y = y + dy
    SelectRect.display = True

@window.event
def on_mouse_release(x, y, button, modifiers):
    SelectRect.display = False

@window.event
def on_draw():
    window.clear()
    if SelectRect.display:
        draw_rectangle(SelectRect.start_x, SelectRect.start_y, SelectRect.end_x, SelectRect.end_y)
pyglet.app.run()