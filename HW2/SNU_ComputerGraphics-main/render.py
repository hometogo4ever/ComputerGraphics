import pyglet
from pyglet import window, app, shapes
from pyglet.window import mouse,key

from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.gl import GL_TRIANGLES
from pyglet.math import Mat4, Vec3, Vec4
from pyglet.gl import *

import shader
from primitives import CustomGroup, Cube

BEZIER_MATRIX = Mat4((1, 0, 0, 0, -3, 3, 0, 0, 3, -6, 3, 0, -1, 3, -3, 1))
BEZIER_TRANS = Mat4((1, -3, 3, -1, 0,3,-6,3, 0,0,3,-3, 0,0,0,1))
BSPLINE_MATRIX = Mat4((1/6, 4/6, 1/6, 0, -3/6, 0, 3/6, 0, 3/6, -6/6, 3/6, 0, -1/6, 3/6, -3/6, 1/6))
BSPLINE_TRANS = Mat4((1/6, -3/6, 3/6, -1/6, 4/6, 0, -6/6, 3/6, 1/6, 3/6, 3/6, -3/6, 0, 0, 0, 1/6))
SAMPLE = 11
STEP = 2
CONTROL_BLOCK = Cube(Vec3(0.05, 0.05, 0.05))
ID_MAT = Mat4.from_translation(vector=Vec3(x=0, y=0, z=0))
COLVEC = [255, 255, 100, 255]
def surf_color(n):
    return ('Bn', COLVEC*n)

def intotxt(il, vl, l):
    txt = ''
    for i in range(int(len(vl)/3)):
        txt += 'v '
        for k in range(3):
            txt += str(vl[3*i+k])
            txt += ' '
        txt += '\n'
    if il != None:
        for j in range(int(len(il)/l)):
            txt += 'f '
            for ik in range(l):
                txt += str(il[j*l + ik]+1)
                txt += ' '
            txt += '\n'
    return txt



class RenderWindow(pyglet.window.Window):
    '''
    inherits pyglet.window.Window which is the default render window of Pyglet
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MOD = 1
        self.batch = pyglet.graphics.Batch()
        '''
        View (camera) parameters
        '''
        self.cam_eye = Vec3(-5,5,5)
        self.cam_target = Vec3(0,0,0)
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
        self.extra = args
        self.nowon = (-1, Vec3(0,0,0))
        self.animate = False
        self.tar = (-1,-1)
    def modset(self, mode):
        self.MOD = mode
    def colorset(self, r, g, b):
        COLVEC[0] = r
        COLVEC[1] = g
        COLVEC[2] = b
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
    def atclick(self, mx, my):
        t = list(self.shapes[0].indexed_vertices_list.vertices)
        view_proj = self.proj_mat @ self.view_mat
        for i in range(int(len(t)/3)):
            vec = Vec4(t[3*i], t[3*i+1], t[3*i+2], 1)
            vec = view_proj @ vec
            cx = (vec[0]/vec[3] + 1) * int(self.width)/2
            cy = (vec[1]/vec[3] + 1) * int(self.height)/2
            distance = ((cx-mx)**2 + (cy-my)**2) ** 0.5
            if distance < 10:
                if self.nowon[0] < 0:
                    trans = Mat4.from_translation(Vec3(t[3*i], t[3*i+1], t[3*i+2])) @ Mat4.from_scale(Vec3(5, 5, 5)) @ Mat4.from_translation(Vec3(-t[3*i], -t[3*i+1], -t[3*i+2]))
                    sp = self.shapes[i+1]
                    sp.transform_mat = trans @ sp.transform_mat
                    self.nowon = (i, Vec3(t[3*i], t[3*i+1], t[3*i+2]))
                return self.nowon
        if self.nowon[0] != -1:
            trans =  Mat4.from_translation(self.nowon[1]) @ Mat4.from_scale(Vec3(0.2, 0.2, 0.2)) @ Mat4.from_translation(self.nowon[1] * -1)
            sp = self.shapes[self.nowon[0]+1]
            sp.transform_mat = trans @ sp.transform_mat
        self.nowon = (-1, Vec3(0,0,0))
        return self.nowon
    def updatespline(self, vlist):
        surf = self.shapes[-1]
        ln = self.shapes[-2]
        xt = []
        yt = []
        zt = []
        for i in range(int(len(vlist)/3)):
            xt.append(vlist[3*i])
            yt.append(vlist[3*i+1])
            zt.append(vlist[3*i+2])
        if self.MOD:
            changeOfBasis = BEZIER_MATRIX
            changeOfBasisT = BEZIER_TRANS
        else:
            changeOfBasis = BSPLINE_MATRIX
            changeOfBasisT = BSPLINE_TRANS    
        matX = changeOfBasisT @ Mat4(xt) @ changeOfBasis
        matY = changeOfBasisT @ Mat4(yt) @ changeOfBasis
        matZ = changeOfBasisT @ Mat4(zt) @ changeOfBasis

        vlistS = []
        for i in range(SAMPLE):
            ir = i/(SAMPLE-1)
            vecx = Vec4(1, ir, ir**2, ir**3)
            for j in range(SAMPLE):
                jr = j/(SAMPLE-1)
                vecy = Vec4(1, jr, jr**2, jr**3)
                gx = matX @ vecy
                gy = matY @ vecy
                gz = matZ @ vecy

                px = vecx.dot(gx)
                py = vecx.dot(gy)
                pz = vecx.dot(gz)
                vlistS += [px, py, pz]
        garbage = pyglet.graphics.get_default_batch()
        self.batch.migrate(surf.indexed_vertices_list, GL_TRIANGLE_FAN, None, garbage)
        self.batch.migrate(ln.indexed_vertices_list, GL_TRIANGLE_FAN, None, garbage)
        surf.indexed_vertices_list = surf.shader_program.vertex_list_indexed(int(len(vlistS)/3), GL_TRIANGLE_FAN, batch=self.batch, 
                                                                                group = surf, 
                                                                                indices = surf.indices, 
                                                                                vertices = ('f', vlistS),
                                                                                colors = surf_color(int(len(vlistS)/3)))
        ln.indexed_vertices_list = ln.shader_program.vertex_list_indexed(int(len(vlistS)/3), GL_LINES, batch=self.batch,
                                                                                group = ln,
                                                                                indices = ln.indices,
                                                                                vertices = ('f', vlistS))
    def inversevec(self, x, y, dx, dy):
        distance = ((dx-x)**2+(dy-y)**2)**0.5
        view_proj = self.proj_mat @ self.view_mat
        if distance > 1:
            nx = ((dx-x)*2/self.width) * 2
            ny = ((dy-y)*2/self.height) * 2
            vec = Vec4(nx, ny, 0, 0)
            vec = view_proj.__invert__() @ vec
            newvec = Vec3(vec[0], vec[1], vec[2])
            return newvec * 0.1
        else:
            return Vec3(0,0,0)
    def click(self, x, y):
        if self.tar[0] < 0:
            self.tar = (x, y)
    def declick(self):
        k = self.nowon
        cb = self.shapes[k[0]+1]
        trans =  Mat4.from_translation(k[1]) @ Mat4.from_scale(Vec3(0.2, 0.2, 0.2)) @ Mat4.from_translation(k[1] * -1)
        cb.transform_mat = trans @ cb.transform_mat
        self.tar = (-1,-1)
        self.nowon = (-1,Vec3(0,0,0))
    def clickmove(self,x, y):
        if (self.nowon[0]) >= 0:
            vec = self.inversevec(self.tar[0], self.tar[1], x, y)

            if vec != Vec3(0,0,0):
                    trans = Mat4.from_translation(vec)
                    i = self.nowon[0]
                    self.nowon = (i, self.nowon[1] + vec)
                    shape = self.shapes[0]
                    ivl = shape.indexed_vertices_list
                    newVertices = list(ivl.vertices)
                    vec = Vec4(newVertices[3*i], newVertices[3*i+1], newVertices[3*i+2], 1)
                    vec = trans @ vec
                    garbage = pyglet.graphics.get_default_batch()
                    self.batch.migrate(ivl, GL_TRIANGLE_FAN, None, garbage)
                    newVertices[3*i] = vec[0]
                    newVertices[3*i+1] = vec[1]
                    newVertices[3*i+2] = vec[2]
                    shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(int(len(newVertices)/3), GL_LINES, batch=self.batch, 
                                                                                        group = shape, 
                                                                                        indices = shape.indices, 
                                                                                        vertices = ('f', newVertices))
                    self.shapes[0] = shape
                    cb = self.shapes[i+1]
                    cb.transform_mat = trans @ cb.transform_mat
                    self.updatespline(newVertices)
    def add_polygon(self, transform, indice, vertice, mode=False):
        shape = CustomGroup(transform, len(self.shapes))
        if mode:
            shape.indices = indice
            shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(int(len(vertice)/3), GL_LINES, batch=self.batch, 
                                                                               group = shape, 
                                                                               indices = indice, 
                                                                               vertices = ('f', vertice))
        else:
            shape.indices = indice
            shape.indexed_vertices_list = shape.shader_program.vertex_list_indexed(int(len(vertice)/3), GL_TRIANGLE_FAN, batch=self.batch, 
                                                                               group = shape, 
                                                                               indices = indice, 
                                                                               vertices = ('f', vertice),
                                                                               colors = surf_color(int(len(vertice)/3)))
        self.shapes.append(shape)
        if len(self.shapes) == 1:
            for i in range(int(len(vertice)/3)):
                trans = Mat4.from_translation(Vec3(vertice[3*i], vertice[3*i+1], vertice[3*i+2]))
                self.add_shape(trans, CONTROL_BLOCK.vertices, CONTROL_BLOCK.indices, CONTROL_BLOCK.colors)
            
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
        rotate_mat = Mat4.from_rotation(angle = -0.5, vector = self.cam_vup)
        eye4 = Vec4(self.cam_eye[0], self.cam_eye[1], self.cam_eye[2], 1)
        eye4 = Mat4.from_translation(self.cam_target) @ rotate_mat @ Mat4.from_translation(self.cam_target * -1) @ eye4
        self.cam_eye = Vec3(eye4[0], eye4[1], eye4[2])
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def eop(self):
        rotate_mat = Mat4.from_rotation(angle = 0.5, vector = self.cam_vup)
        eye4 = Vec4(self.cam_eye[0], self.cam_eye[1], self.cam_eye[2], 1)
        eye4 = Mat4.from_translation(self.cam_target) @ rotate_mat @ Mat4.from_translation(self.cam_target * -1) @ eye4
        self.cam_eye = Vec3(eye4[0], eye4[1], eye4[2])
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def rop(self):
        vec = self.cam_vup.cross(self.cam_eye-self.cam_target)
        rotate_mat = Mat4.from_rotation(angle = -0.5, vector = vec.normalize())
        eye4 = Vec4(self.cam_eye[0], self.cam_eye[1], self.cam_eye[2], 1)
        eye4 = Mat4.from_translation(self.cam_target) @ rotate_mat @ Mat4.from_translation(self.cam_target * -1) @ eye4
        self.cam_eye = Vec3(eye4[0], eye4[1], eye4[2])
        self.view_mat = Mat4.look_at(
            self.cam_eye, target=self.cam_target, up=self.cam_vup)
    def fop(self):
        vec = self.cam_vup.cross(self.cam_eye-self.cam_target)
        rotate_mat = Mat4.from_rotation(angle = 0.5, vector = vec.normalize())
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


