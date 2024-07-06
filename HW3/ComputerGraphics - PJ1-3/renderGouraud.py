import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key

from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_TRIANGLES
from pyglet.math import Mat4, Vec3, Vec4
from pyglet.gl import *

import shader
from primitives import CustomGroup
COLVEC = [255,255, 255, 255]

K_a = (0.1, 0.1, 0.1)
K_d = (0.5, 0.5, 0.5)
K_s = (0.8, 0.8, 0.8)
I_intensity = 100
I_ambient = 2
Shineness = 4

def surf_color(n):
    return ('Bn', COLVEC*n)

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
        self.cam_eye = Vec3(10,10,10)
        self.cam_target = Vec3(0,0,0)
        self.cam_vup = Vec3(0,1,0)
        self.light_source = Vec3(7, 8, 7)
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

        self.animate = False

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
        for i, shape in enumerate(self.shapes):
            '''
            Update position/orientation in the scene. In the current setting, 
            shapes created later rotate faster while positions are not changed.
            '''
            if self.animate:
                rotate_angle = dt
                rotate_axis = Vec3(0,0,1)
                rotate_mat = Mat4.from_rotation(angle = rotate_angle, vector = rotate_axis)
                
                shape.transform_mat @= rotate_mat

                # # Example) You can control the vertices of shape.
                # shape.indexed_vertices_list.vertices[0] += 0.5 * dt

            '''
            Update view and projection matrix. There exist only one view and projection matrix 
            in the program, so we just assign the same matrices for all the shapes
            '''
            shape.shader_program['view_proj'] = view_proj

    def on_resize(self, width, height):
        glViewport(0, 0, *self.get_framebuffer_size())
        self.proj_mat = Mat4.perspective_projection(
            aspect = width/height, z_near=self.z_near, z_far=self.z_far, fov = self.fov)
        return pyglet.event.EVENT_HANDLED

    def add_shape(self, transform, vertice, indice, color):
        
        '''
        Assign a group for each shape
        '''
        shape = CustomGroup(transform, len(self.shapes))
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(len(vertice)//3, GL_TRIANGLES,
                        batch = self.batch,
                        group = shape,
                        indices = indice,
                        vertices = ('f', vertice),
                        colors = ('Bn', color))
        self.shapes.append(shape)
    
    def add_wire(self, transform, indice, vertice):
        shape = CustomGroup(transform, len(self.shapes))
        shape.indices = indice
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(int(len(vertice)/3), GL_LINES, batch=self.batch, 
                                                                            group = shape, 
                                                                            indices = indice, 
                                                                            vertices = ('f', vertice))
        self.shapes.append(shape)
    def add_polygon(self, transform, indice, indexnormal, vertice, temp):
        shape = CustomGroup(transform, len(self.shapes), 'gouraud')
        print(len(indice))
        print(len(indexnormal))
        print(len(vertice))
        shape.indices = indice
        color = [100,100,100,255] * (len(vertice)//3)

        """
        Phong
        for v in range(int(len(vertice)/3)):
            p = vertice[3*v:3*v+3]
            n = indexnormal[3*v:3*v + 3]
            weightP = Vec3(p[0], p[1], p[2])
            viewVec = (self.cam_eye - weightP).normalize()
            lightVec = (self.light_source - weightP).normalize()
            normalVec = Vec3(n[0], n[1], n[2])
            reflectVec = normalVec.__mul__(2*(lightVec.dot(normalVec))) - lightVec
            distance = abs(self.light_source - weightP)
        
            for c in range(3):
                col = COLVEC[c]
                i1 = K_s[c] * ((reflectVec.dot(viewVec)) ** Shineness)
                nl = normalVec.dot(lightVec)
                if nl > 0:
                    i2 = K_d[c] * nl
                else:
                    i2 = 0
                iout = (i1+ i2) * I_intensity / (distance ** 2)
                i3 = K_a[c]
                iout += i3
                color[4*v + c] = int(col * iout)

        texture_cord = []
        for idx in range(int(len(indice)/3)):
            txture = textureidx[3*idx:3*idx+3]
            for tidx in txture:
                tx = texturecord[2*tidx]
                ty = texturecord[2*tidx+1]
                texture_cord += [tx, ty]
        """

        shape.set_state()
        shape.shader_program["lightposition"] = self.light_source
        shape.shader_program["viewposition"] = self.cam_eye
        shape.shader_program["K_a"] = K_a
        shape.shader_program["K_d"] = K_d
        shape.shader_program["K_s"] = K_s
        shape.shader_program["I_intensity"] = I_intensity
        shape.shader_program["I_ambient"] = I_ambient
        shape.shader_program["shineness"] = Shineness    
        shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(int(len(vertice)/3), GL_TRIANGLES, batch=self.batch, 
                                                                            group = shape, 
                                                                            indices = indice, 
                                                                            vertices = ('f', vertice),
                                                                            colors = ('Bn',color),
                                                                            nmal = ('f', indexnormal))
        self.shapes.append(shape)
       
    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60)
        pyglet.app.run()
    def aop(self):
        transvec = self.cam_eye - self.cam_target
        transvec = transvec.cross(self.cam_vup)
        transvec = transvec.normalize()
        self.cam_eye += transvec
        self.cam_target += transvec
        # 1. Create a view matrix
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def dop(self):
        transvec = self.cam_eye - self.cam_target
        transvec = transvec.cross(self.cam_vup)
        transvec = transvec.normalize()
        self.cam_eye -= transvec
        self.cam_target -= transvec
        # 1. Create a view matrix
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def wop(self):
        transvec = self.cam_eye - self.cam_target
        transvec = transvec.cross(self.cam_vup)
        transvec = transvec.cross(self.cam_vup)
        transvec = transvec.normalize()
        self.cam_eye += transvec
        self.cam_target += transvec
        # 1. Create a view matrix
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def sop(self):
        transvec = self.cam_eye - self.cam_target
        transvec = transvec.cross(self.cam_vup)
        transvec = transvec.cross(self.cam_vup)
        transvec = transvec.normalize()
        self.cam_eye -= transvec
        self.cam_target -= transvec
        # 1. Create a view matrix
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def qop(self):
        rotate_mat = Mat4.from_rotation(angle = -0.1, vector = self.cam_vup)
        eye4 = Vec4(self.cam_eye[0], self.cam_eye[1], self.cam_eye[2], 1)
        eye4 = Mat4.from_translation(self.cam_target) @ rotate_mat @ Mat4.from_translation(self.cam_target * -1) @ eye4
        self.cam_eye = Vec3(eye4[0], eye4[1], eye4[2])
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def eop(self):
        rotate_mat = Mat4.from_rotation(angle = 0.1, vector = self.cam_vup)
        eye4 = Vec4(self.cam_eye[0], self.cam_eye[1], self.cam_eye[2], 1)
        eye4 = Mat4.from_translation(self.cam_target) @ rotate_mat @ Mat4.from_translation(self.cam_target * -1) @ eye4
        self.cam_eye = Vec3(eye4[0], eye4[1], eye4[2])
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def rop(self):
        vec = self.cam_vup.cross(self.cam_eye-self.cam_target)
        rotate_mat = Mat4.from_rotation(angle = -0.1, vector = vec.normalize())
        eye4 = Vec4(self.cam_eye[0], self.cam_eye[1], self.cam_eye[2], 1)
        eye4 = Mat4.from_translation(self.cam_target) @ rotate_mat @ Mat4.from_translation(self.cam_target * -1) @ eye4
        self.cam_eye = Vec3(eye4[0], eye4[1], eye4[2])
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def fop(self):
        vec = self.cam_vup.cross(self.cam_eye-self.cam_target)
        rotate_mat = Mat4.from_rotation(angle = 0.1, vector = vec.normalize())
        eye4 = Vec4(self.cam_eye[0], self.cam_eye[1], self.cam_eye[2], 1)
        eye4 = Mat4.from_translation(self.cam_target) @ rotate_mat @ Mat4.from_translation(self.cam_target * -1) @ eye4
        self.cam_eye = Vec3(eye4[0], eye4[1], eye4[2])
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def top(self):
        scale_mat = Mat4.from_scale(Vec3(0.8, 0.8, 0.8))
        eye4 = Vec4(self.cam_eye[0], self.cam_eye[1], self.cam_eye[2], 1)
        eye4 = Mat4.from_translation(self.cam_target) @ scale_mat @ Mat4.from_translation(self.cam_target * -1) @ eye4
        self.cam_eye = Vec3(eye4[0], eye4[1], eye4[2])
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def gop(self):
        scale_mat = Mat4.from_scale(Vec3(1.25,1.25, 1.25))
        eye4 = Vec4(self.cam_eye[0], self.cam_eye[1], self.cam_eye[2], 1)
        eye4 = Mat4.from_translation(self.cam_target) @ scale_mat @ Mat4.from_translation(self.cam_target * -1) @ eye4
        self.cam_eye = Vec3(eye4[0], eye4[1], eye4[2])
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    