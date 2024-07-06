import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key

from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_TRIANGLES
from pyglet.math import Mat4, Vec3, Vec4
from pyglet.gl import *

import shader
from primitives import CustomGroup



class RenderWindow(pyglet.window.Window):
    '''
    inherits pyglet.window.Window which is the default render window of Pyglet
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        '''
        View (camera) parameters
        '''
        self.cam_eye = Vec3(20,15, 20)
        self.cam_target = Vec3(5,0,0)
        self.cam_vup = Vec3(0,1,0)
        self.view_mat = None
        '''
        Projection parameters
        '''
        self.z_near = 0.1
        self.z_far = 100
        self.fov = 60
        self.proj_mat = None

        self.shapes = []
        self.setup()

        self.animate = True
        self.counter = 0
        self.angle = 0

    def setup(self) -> None:
        self.set_minimum_size(width = 400, height = 300)
        self.set_mouse_visible(True)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        # 1. Create a view matrix
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
        
        # 2. Create a projection matrix 
        self.proj_mat = Mat4.perspective_projection(
            aspect = self.width/self.height, 
            z_near=self.z_near, 
            z_far=self.z_far, 
            fov = self.fov)

    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()
    def update(self,dt) -> None:
        view_proj = self.proj_mat @ self.view_mat
        (x0, y0, z0,w0) = self.shapes[0].transform_mat @ Vec4(0,0,0,1)
        for i, shape in enumerate(self.shapes):
            '''
            Update position/orientation in the scene. In the current setting, 
            shapes created later rotate faster while positions are not changed.
            '''

            # Initial Begin
            if (self.counter == 0) and hash(shape) >= 0:
                trns = Mat4.from_translation(Vec3(-60, 0, 0))
                shape.transform_mat = trns @ shape.transform_mat
                if hash(shape) >= 2:
                    v = Vec4(0, 1.5, 0, 1)
                    newv = shape.transform_mat @ v
                    (x, y, z, w) = newv
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    angle = ((hash(shape) % 2)*2-1) * 45
                    axis = Vec3(0,0,1)
                    rt1 = Mat4.from_rotation(angle, axis)
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt1 @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
                    self.angle += angle/30
            # S1 : Walking Into
            elif (self.counter < 253):
                if hash(shape) >= 0:
                    trns = Mat4.from_translation(Vec3(dt*15, 0, 0))
                    shape.transform_mat = trns @ shape.transform_mat
                if hash(shape) >= 2:
                    v = Vec4(0,1.5,0,1)
                    if hash(shape) == 7:
                        v += Vec4(-1.5, 1.5, 0, 0)
                    newv = shape.transform_mat @ v
                    (x, y, z, w) = newv
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    if ((self.counter // 20) % 2):
                        k = 1
                    else:
                        k = -1
                    angle = ((hash(shape) % 2)*2-1) * dt * k * 5
                    axis = Vec3(0,0,1)
                    rt1 = Mat4.from_rotation(angle, axis)
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt1 @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
                    self.angle += angle
            
            #S2 : Building Block
            elif self.counter < 283 or (self.counter >= 323 and self.counter < 353) or (self.counter >= 393 and self.counter < 423):
                if hash(shape) >= 0:
                    trns = Mat4.from_translation(Vec3(-x0, -y0, -z0))
                    rt = Mat4.from_rotation(dt*3, Vec3(0,1,0))
                    trns2 = Mat4.from_translation(Vec3(x0, y0, z0))
                    shape.transform_mat = trns @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
            elif self.counter >= 463 and self.counter <= 483:
                if hash(shape) == 1:
                    (x, y, z, w) = shape.transform_mat @ Vec4(0,-1,0,1)
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    rt = Mat4.from_rotation(dt*1.5, Vec3(-1,0,0))
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
            elif self.counter < 523:
                print(hash(shape))
                if hash(shape) == -5 and self.counter == 310:
                    shape.transform_mat = Mat4.from_translation(Vec3(0, -16, 0)) @ shape.transform_mat
                if hash(shape) == -6 and self.counter == 380:
                    shape.transform_mat = Mat4.from_translation(Vec3(0, -16, 0)) @ shape.transform_mat
                if hash(shape) == -7 and self.counter == 430:
                    shape.transform_mat = Mat4.from_translation(Vec3(0, -19, 0)) @ shape.transform_mat
                if hash(shape) == -8 and self.counter == 510:
                    shape.transform_mat = Mat4.from_translation(Vec3(0, -17, 0)) @ shape.transform_mat
                if hash(shape) == 3 or hash(shape) == 7:
                    if self.counter < 293:
                        axis = Vec3(0,0,1)
                    elif self.counter < 303:
                        axis = Vec3(0,1,0)
                    elif self.counter < 313:
                        axis = Vec3(0,-1,0)
                    elif self.counter < 323:
                        axis = Vec3(0,0,-1)
                    
                    elif self.counter < 363:
                        axis = Vec3(1,0,0)
                    elif self.counter < 373:
                        axis = Vec3(0,1,0)
                    elif self.counter < 383:
                        axis = Vec3(0,-1,0)
                    elif self.counter < 393:
                        axis = Vec3(-1,0,0)
                    
                    elif self.counter < 433:
                        axis = Vec3(0,0,-1)
                    elif self.counter < 443:
                        axis = Vec3(0,1,0)
                    elif self.counter < 453:
                        axis = Vec3(0,-1,0)
                    elif self.counter < 463:
                        axis = Vec3(0,0,1)
                    
                    elif self.counter < 493:
                        axis = Vec3(0,0,-1)
                    elif self.counter < 503:
                        axis = Vec3(0,1,0)
                    elif self.counter < 513:
                        axis = Vec3(0,-1,0)
                    elif self.counter < 523:
                        axis = Vec3(0,0,1)
                    v = Vec4(0, 1.5, 0, 1)
                    if hash(shape) == 7:
                        v += Vec4(-1.5, 1.5, 0, 0)
                    (x,y,z,w) = shape.transform_mat @ v
                    rt = Mat4.from_rotation(dt*9, axis)
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
            #S3 : Breaking Block
            elif self.counter >= 600 and self.counter < 850:
                if hash(shape) == 3 or hash(shape) == 7:
                    v = Vec4(0, 1.5, 0, 1)
                    if hash(shape) == 7:
                        v += Vec4(-1.5, 1.5, 0, 0)
                    (x,y,z,w) = shape.transform_mat @ v
                    if (self.counter < 613):
                        axis = Vec3(-1,0,0)
                    else:
                        axis = Vec3(2*((self.counter // 8)%2)-1, 0, 0)
                    rt = Mat4.from_rotation(dt*10, axis)
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
                if self.counter > 800 and self.counter < 840:
                    if hash(shape) == -2:
                        trans = Mat4.from_translation(Vec3(0,-dt*30, 0))
                        shape.transform_mat = trans @ shape.transform_mat
            elif self.counter > 880 and self.counter < 889:
                if hash(shape) == 3 or hash(shape) == 7: 
                    v = Vec4(0, 1.5, 0, 1)
                    if hash(shape) == 7:
                        v += Vec4(-1.5, 1.5, 0, 0)
                    (x,y,z,w) = shape.transform_mat @ v
                    rt = Mat4.from_rotation(dt*10, Vec3(1,0,0))
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
                elif hash(shape) == 1:
                    (x, y, z, w) = shape.transform_mat @ Vec4(0,-1,0,1)
                    rt = Mat4.from_rotation(dt*5, Vec3(1,0,0))
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
            elif (self.counter >= 900 and self.counter < 930):
                if hash(shape) >= 0:
                    trns = Mat4.from_translation(Vec3(-x0, -y0, -z0))
                    rt = Mat4.from_rotation(dt*3, Vec3(0,1,0))
                    trns2 = Mat4.from_translation(Vec3(x0, y0, z0))
                    shape.transform_mat = trns @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
            elif self.counter > 930 and self.counter < 1000:
                if hash(shape) == 1:
                    (x, y, z, w) = shape.transform_mat @ Vec4(0,-1,0,1)
                    if self.counter < 950:
                        v = 1
                    elif self.counter > 980:
                        v = -1
                    if self.counter < 950 or self.counter > 980:
                        rt = Mat4.from_rotation(dt*3, Vec3(v,0,0))
                        trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                        trns2 = Mat4.from_translation(Vec3(x, y, z))
                        shape.transform_mat = trns1 @ shape.transform_mat
                        shape.transform_mat = rt @ shape.transform_mat
                        shape.transform_mat = trns2 @ shape.transform_mat
            elif self.counter > 1000 and self.counter < 1018:
                if hash(shape) == 3 or hash(shape) == 7:
                    if self.counter < 1005:
                        axis = Vec3(-1,0,0)
                    elif self.counter < 1010:
                        axis = Vec3(0,1,0)
                    elif self.counter < 1015:
                        axis = Vec3(0,-1,0)
                    elif self.counter < 1018:
                        axis = Vec3(1,0,0)
                    v = Vec4(0, 1.5, 0, 1)
                    if hash(shape) == 7:
                        v += Vec4(-1.5, 1.5, 0, 0)
                    (x,y,z,w) = shape.transform_mat @ v
                    rt = Mat4.from_rotation(dt*18, axis)
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
            elif self.counter > 1020 and self.counter < 1030:
                if hash(shape) == -2:
                    if self.counter < 1025:
                        trns = Mat4.from_translation(Vec3(0,dt*10,0))
                    elif self.counter < 1030:
                        trns = Mat4.from_translation(Vec3(0,-dt*10,0))
                    shape.transform_mat = trns @ shape.transform_mat
            elif self.counter > 1040 and self.counter < 1060:
                if hash(shape) >= 0:
                    if self.counter < 1050:
                        trns = Mat4.from_translation(Vec3(0,dt*10,0))
                    elif self.counter < 1060:
                        trns = Mat4.from_translation(Vec3(0,-dt*10,0))
                    shape.transform_mat = trns @ shape.transform_mat
            elif self.counter > 1070 and self.counter < 1130:
                if hash(shape) >= 0:
                    trns = Mat4.from_translation(Vec3(-x0, -y0, -z0))
                    rt = Mat4.from_rotation(dt*3, Vec3(0,1,0))
                    trns2 = Mat4.from_translation(Vec3(x0, y0, z0))
                    shape.transform_mat = trns @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
            elif self.counter == 1300:
                if hash(shape) >= 0:
                    trns = Mat4.from_translation(Vec3(120, 0, 0))
                    shape.transform_mat = trns @ shape.transform_mat
            elif self.counter > 1130 and self.counter < 1376:
                if hash(shape) >= 0:
                    trns = Mat4.from_translation(Vec3(-dt*30, 0, 0))
                    shape.transform_mat = trns @ shape.transform_mat
                if hash(shape) >= 2:
                    v = Vec4(0,1.5,0,1)
                    if hash(shape) == 7:
                        v += Vec4(-1.5, 1.5, 0, 0)
                    newv = shape.transform_mat @ v
                    (x, y, z, w) = newv
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    if ((self.counter // 5) % 2):
                        k = 1
                    else:
                        k = -1
                    angle = ((hash(shape) % 2)*2-1) * dt * k * 20
                    axis = Vec3(0,0,1)
                    rt1 = Mat4.from_rotation(angle, axis)
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt1 @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
                    self.angle += angle
                if self.counter > 1350 and self.counter < 1370:
                    if hash(shape) == -2:
                        (x, y, z, w)= shape.transform_mat @ Vec4(0,0.5, 0)
                        trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                        rt1 = Mat4.from_rotation(dt*3, Vec3(-1,0,0))
                        trns2 = Mat4.from_translation(Vec3(x, y, z))
                        t = Mat4.from_translation(Vec3(0,0,-dt*5))
                        shape.transform_mat = trns1 @ shape.transform_mat
                        shape.transform_mat = rt1 @ shape.transform_mat
                        shape.transform_mat = trns2 @ shape.transform_mat
                        shape.transform_mat = t @ shape.transform_mat
            elif self.counter > 1390 and self.counter < 1450:
                if hash(shape) >= 0:
                    trns = Mat4.from_translation(Vec3(-x0, -y0, -z0))
                    rt = Mat4.from_rotation(dt*3.6, Vec3(0,1,0))
                    trns2 = Mat4.from_translation(Vec3(x0, y0, z0))
                    shape.transform_mat = trns @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
            elif self.counter > 1490 and self.counter < 1500:
                if hash(shape) == -2:
                    sz = Mat4.from_scale(Vec3(1.05, 1.05, 1.05))
                    (x, y, z, w)= shape.transform_mat @ Vec4(0,0.5, 0)
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = sz @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
            elif self.counter > 1510 and self.counter < 1530:
                if hash(shape) >= 0:
                    if self.counter < 1520:
                        trns = Mat4.from_translation(Vec3(0,dt*10,0))
                    elif self.counter < 1530:
                        trns = Mat4.from_translation(Vec3(0,-dt*10,0))
                    shape.transform_mat = trns @ shape.transform_mat
            elif self.counter >= 1540 and self.counter <= 1580:
                if hash(shape) == 1:
                    (x, y, z, w) = shape.transform_mat @ Vec4(0,-1,0,1)
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    rt = Mat4.from_rotation(dt*2, Vec3(0,0,1))
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
            elif self.counter >= 1590 and self.counter < 1607:
                if hash(shape) == 3 or hash(shape) == 7:
                    v = Vec4(0, 1.5, 0, 1)
                    if hash(shape) == 7:
                        v += Vec4(-1.5, 1.5, 0, 0)
                    (x,y,z,w) = shape.transform_mat @ v
                    rt = Mat4.from_rotation(dt*10, Vec3(0,0,1))
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
            elif self.counter > 1610 and self.counter < 1800:
                if hash(shape) == 7:
                    (x,y,z,w) = shape.transform_mat @ Vec4(-1.5, 0, 0, 1)
                    rt = Mat4.from_rotation(dt*25, Vec3(0,1,0))
                    trns1 = Mat4.from_translation(Vec3(-x, -y, -z))
                    trns2 = Mat4.from_translation(Vec3(x, y, z))
                    shape.transform_mat = trns1 @ shape.transform_mat
                    shape.transform_mat = rt @ shape.transform_mat
                    shape.transform_mat = trns2 @ shape.transform_mat
                if self.counter > 1700:
                    if hash(shape) >= 0:
                        trns = Mat4.from_translation(Vec3(0,dt*20,0))
                        shape.transform_mat = trns @ shape.transform_mat
            elif self.counter > 1800 and self.counter < 1850:
                if hash(shape) != 7 and hash(shape) >= 0:
                    trns = Mat4.from_translation(Vec3(0,-dt*40, 0))
                    shape.transform_mat = trns @ shape.transform_mat
            elif self.counter > 1850 and self.counter < 1860:
                if hash(shape) != 7 and hash(shape) >= 0:
                    rt = Mat4.from_rotation(-dt*9, Vec3(1,0,0))
                    shape.transform_mat = rt @ shape.transform_mat
            
            
            

            
            #S4 : Falling TNT Sphere

            shape.shader_program['view_proj'] = view_proj
        self.counter += 1

    def on_resize(self, width, height):
        glViewport(0, 0, *self.get_framebuffer_size())
        self.proj_mat = Mat4.perspective_projection(
            aspect = width/height, z_near=self.z_near, z_far=self.z_far, fov = self.fov)
        return pyglet.event.EVENT_HANDLED

    def add_shape(self, transform, sp, num):
        
        '''
        Assign a group for each shape
        '''
        shape = CustomGroup(transform, num)
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(sp.vertices)//3, GL_TRIANGLES,
                        batch = self.batch,
                        group = shape,
                        indices = sp.indices,
                        vertices = ('f', sp.vertices),
                        colors = ('Bn', sp.colors))
        self.shapes.append(shape)
         
    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()

    