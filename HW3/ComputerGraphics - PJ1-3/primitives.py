import pyglet
from pyglet import window, app, shapes
from pyglet.math import Mat4, Vec3, Vec4
import math
from pyglet.gl import *

import shader

class CustomGroup(pyglet.graphics.Group):
    '''
    To draw multiple 3D shapes in Pyglet, you should make a group for an object.
    '''
    def __init__(self, transform_mat: Mat4, order, mode = 'default'):
        super().__init__(order)

        '''
        Create shader program for each shape
        '''
        if mode == 'default':
            self.shader_program = shader.create_program(
                shader.vertex_source_default, shader.fragment_source_default
            )
        elif mode == 'texture':
            self.shader_program = shader.create_program(
                shader.vertex_source_phongtex, shader.fragment_source_phongtex
            )
        elif mode == 'texturenormal':
            self.shader_program = shader.create_program(
                shader.vertex_source_phongtexN, shader.fragment_source_phongtexN
            )
        elif mode == 'phong':
            self.shader_program = shader.create_program(
                shader.vertex_source_phong, shader.fragment_source_phong
            )
        elif mode == 'gouraud':
            self.shader_program = shader.create_program(
                shader.vertex_source_gourang, shader.fragment_source_gourang
            )

        self.transform_mat = transform_mat
        self.indexed_vertices_list = None
        self.shader_program.use()

    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program['model'] = model

    def unset_state(self):
        self.shader_program.stop()

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.order == other.order and
                self.parent == other.parent)
    
    def __hash__(self):
        return hash((self.order)) 
    
class CustomTextureGroup(CustomGroup):
    def add_texture(self, texture):
        self.texture = texture
    def set_state(self):
        self.shader_program.use()
        for v in range(len(self.texture)):
            text = self.texture[v]
            tid = GL_TEXTURE0 + v
            glActiveTexture(tid)
            glBindTexture(text.target, text.id)
        model = self.transform_mat
        self.shader_program['model'] = model
class Cube:
    '''
    default structure of cube
    '''
    def __init__(self, scale=1.0):
        self.vertices = [-0.5, -0.5, 0.5,
            0.5, -0.5, 0.5,
            0.5, 0.5, 0.5,
            -0.5, 0.5, 0.5,
            -0.5, -0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5,0.5,-0.5,
            -0.5,0.5,-0.5]
        self.vertices = [scale[idx%3] * x for idx, x in enumerate(self.vertices)]
    
        self.indices = [0, 1, 2, 2, 3, 0,
                    4, 7, 6, 6, 5, 4,
                    4, 5, 1, 1, 0, 4,
                    6, 7, 3, 3, 2, 6,
                    5, 6, 2, 2, 1, 5,
                    7, 4, 0, 0, 3, 7]
    
        self.colors = (255, 0,  0,255,
                0, 255,  0,255,
                0,   0,255,255,
                255,255,255,255,
                
                255, 0,  0,255,
                0, 255,  0,255,
                0,   0,255,255,
                255,255,255,255)
        
class Sphere:
    '''
    default structure of sphere
    '''
    def __init__(self, stacks, slices, scale=1.0):
        num_triangles = 2 * slices * (stacks - 1)

        self.vertices = []
        self.indices = []
        self.colors = ()

        for i in range(stacks):
            phi0 = 0.5 * math.pi - (i * math.pi) / stacks
            phi1 = 0.5 * math.pi - ((i + 1) * math.pi) / stacks
            coord_v0 = 1.0 - float(i) / stacks
            coord_v1 = 1.0 - float(i + 1) / stacks

            y0 = scale * math.sin(phi0)
            r0 = scale * math.cos(phi0)
            y1 = scale * math.sin(phi1)
            r1 = scale * math.cos(phi1)
            y2 = y1
            y3 = y0

            for j in range(slices):
                theta0 = (j * 2 * math.pi) / slices
                theta1 = ((j + 1) * 2 * math.pi) / slices
                coord_u0 = float(j) / slices
                coord_u1 = float(j + 1) / slices

                x0 = r0 * math.cos(theta0)
                z0 = r0 * math.sin(-theta0)
                u0 = coord_u0
                v0 = coord_v0
                x1 = r1 * math.cos(theta0)
                z1 = r1 * math.sin(-theta0)
                u1 = coord_u0
                v1 = coord_v1
                x2 = r1 * math.cos(theta1)
                z2 = r1 * math.sin(-theta1)
                u2 = coord_u1
                v2 = coord_v1
                x3 = r0 * math.cos(theta1)
                z3 = r0 * math.sin(-theta1)
                u3 = coord_u1
                v3 = coord_v0

                if (i != stacks - 1):
                    self.vertices.append(x0)
                    self.vertices.append(y0)
                    self.vertices.append(z0)

                    self.vertices.append(x1)
                    self.vertices.append(y1)
                    self.vertices.append(z1)

                    self.vertices.append(x2)
                    self.vertices.append(y2)
                    self.vertices.append(z2)
                    
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)
                
                if (i != 0):
                    self.vertices.append(x2)
                    self.vertices.append(y2)
                    self.vertices.append(z2)

                    self.vertices.append(x3)
                    self.vertices.append(y3)
                    self.vertices.append(z3)

                    self.vertices.append(x0)
                    self.vertices.append(y0)
                    self.vertices.append(z0)
                    
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)
                    self.colors += (int(math.cos(phi0) * 255),int(math.cos(theta0) * 255),int(math.sin(phi0)*255),255)

        for i in range(num_triangles*3):
            self.indices.append(i)