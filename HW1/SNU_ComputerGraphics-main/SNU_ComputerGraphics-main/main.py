import pyglet
from pyglet.math import Mat4, Vec3
from time import sleep
from render import RenderWindow
from primitives import Cube,Sphere, CustomGroup
from control import Control
import Image


if __name__ == '__main__':
    width = 1280
    height = 720

    # Render window.
    renderer = RenderWindow(width, height, "Hello Pyglet", resizable = True)   
    renderer.set_location(200, 100)

    # Keyboard/Mouse control. Not implemented yet.
    controller = Control(renderer)
    
    #translate_mat1 = Mat4.from_translation(vector=Vec3(x=v, y=0, z=0))
    #translate_mat2 = Mat4.from_translation(vector=Vec3(x=0, y=0, z=0))
    #translate_mat3 = Mat4.from_translation(vector=Vec3(x=2, y=0, z=0))
    
    #scale_vec = Vec3(x=1, y=1, z=1)

    #cube1 = Cube(scale_vec)
    #cube2 = Cube(Vec3(x=1.5, y=1.5, z=1.5))
    #sphere = Sphere(30,30)
   
    #renderer.add_shape(translate_mat1, cube1.vertices, cube1.indices, cube1.colors)

    head = Cube(Vec3(2, 2, 2))
    body = Cube(Vec3(1, 3, 2))
    arm1 = Cube(Vec3(1, 3, 1))
    arm2 = Cube(Vec3(1, 3, 1))
    leg1 = Cube(Vec3(1, 3, 1))
    leg2 = Cube(Vec3(1, 3, 1))
    stick = Cube(Vec3(3, 0.25, 0.25))
    tnt = Sphere(10, 10, 1)
    b1 = Cube(Vec3(4, 4, 4))
    b2= Cube(Vec3(4, 4, 4))
    b3 = Cube(Vec3(2, 2, 2))
    b4 = Cube(Vec3(2, 2, 2))

    t1 = Mat4.from_translation(Vec3(0,7,0))
    t2 = Mat4.from_translation(Vec3(0,4.5,0))
    t3 = Mat4.from_translation(Vec3(0,4.5,-1.5))
    t4 = Mat4.from_translation(Vec3(0,4.5,1.5))
    t5 = Mat4.from_translation(Vec3(0,1.5, -0.5))
    t6 = Mat4.from_translation(Vec3(0,1.5, 0.5))
    t7 = Mat4.from_translation(Vec3(2.5, 5, 1.5))
    t8 = Mat4.from_translation(Vec3(10,20, 0))

    t9 = Mat4.from_translation(Vec3(5, 20, -10))
    t10 = Mat4.from_translation(Vec3(-5, 20, 0))
    t11 = Mat4.from_translation(Vec3(5, 20, 10))
    t12 = Mat4.from_translation(Vec3(5, 20, 10))


    renderer.add_shape(t1, head, 1)
    renderer.add_shape(t2, body, 0)
    renderer.add_shape(t3, arm1, 2)
    renderer.add_shape(t4, arm2, 3)
    renderer.add_shape(t5, leg1, 4)
    renderer.add_shape(t6, leg2, 5)
    renderer.add_shape(t7, stick, 7)
    renderer.add_shape(t8, tnt, -1)
    renderer.add_shape(t9, b1, -5)
    renderer.add_shape(t10, b2, -6)
    renderer.add_shape(t11, b3, -7)
    renderer.add_shape(t12, b4, -8)
    #draw shapes
    renderer.run()
    
