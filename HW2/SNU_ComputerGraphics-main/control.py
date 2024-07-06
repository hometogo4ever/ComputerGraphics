import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key
from pyglet.math import Mat4, Vec3


class Control:
    """
    Control class controls keyboard & mouse inputs.
    """
    def __init__(self, window):
        window.on_key_press = self.on_key_press
        window.on_key_release = self.on_key_release
        window.on_mouse_motion = self.on_mouse_motion
        window.on_mouse_drag = self.on_mouse_drag
        window.on_mouse_press = self.on_mouse_press
        window.on_mouse_release = self.on_mouse_release
        window.on_mouse_scroll = self.on_mouse_scroll
        self.window = window
        self.SS = 0
        self.setup()
    def sset(self, mode):
        self.SS = mode
    def setup(self):
        pass

    def update(self, vector):
        pass

    def on_key_press(self, symbol, modifier):
        if symbol:
            if symbol == key.W:
                self.window.wop()
            if symbol == key.A:
                self.window.aop()
            if symbol == key.S:
                self.window.sop()
            if symbol == key.D:
                self.window.dop()
            if symbol == key.Q:
                self.window.qop()
            if symbol == key.E:
                self.window.eop()
            if symbol == key.R:
                self.window.rop()
            if symbol == key.F:
                self.window.fop()
            if symbol == key.T:
                self.window.top()
            if symbol == key.G:
                self.window.gop()
    
    def on_key_release(self, symbol, modifier):
        if symbol == pyglet.window.key.ESCAPE:
            vl = list(self.window.shapes[-1].indexed_vertices_list.vertices)
            newcont = ''
            with open('Result.obj', 'r') as f:
                lines = f.readlines()
                vs = int(len(vl)/3)
                for i, j in enumerate(lines):
                    if i < vs:
                        txt = 'v '
                        for k in range(3):
                            txt += str(vl[3*i+k])
                            txt += ' '
                        txt += '\n'
                        newcont += txt
                    else:
                        newcont += j
            with open('Result.obj', 'w') as f:
                f.write(newcont)
            pyglet.app.exit()
        elif symbol == pyglet.window.key.SPACE:
            self.window.animate = not self.window.animate
        # TODO:
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        if self.window.tar == (-1, -1):
            self.window.atclick(x,y)[0]
        # TODO:
        pass

    def on_mouse_press(self, x, y, button, modifier):
        # TODO:
        if self.SS == 1 or self.SS == 0:
            if button and button == mouse.LEFT and self.window.nowon[0] != -1:
                self.window.click(x, y)
        pass

    def on_mouse_release(self, x, y, button, modifier):
        # TODO:
        if self.SS == 1 or self.SS == 0:
            if self.window.tar != (-1, -1):
                self.window.declick()
        pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifier):
        # TODO:
        if self.SS == 1 or self.SS == 0:
            if button:
                if button == mouse.LEFT  and self.window.nowon[0] != -1:
                    self.window.clickmove(x, y)
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # TODO:
        pass