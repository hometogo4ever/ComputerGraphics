import pyglet
from pyglet.math import Mat4, Vec3


#Step2-1 : Gouraud Shading
#from renderGouraud import RenderWindow

#Step2-2 : Phong Shading
#from renderPhong import RenderWindow

#Step3 : Texture
#from renderTexture import RenderWindow

#Step4 : Normal Texture
from renderNormalTexture import RenderWindow

from primitives import Cube,Sphere
from control import Control

def ctwo(ilist2, l):
    ilist = []
    for i in range(int(len(ilist2)/l)):
        ildex = ilist2[i*l:(i+1)*l]
        for j in range(l):
            ilist += [ildex[j-1], ildex[j]]
    return ilist
def cth(ilist2, l):
    ilist = []
    for i in range(int(len(ilist2)/l)):
        ildex = ilist2[i*l:(i+1)*l]
        for j in range(l-2):
            ilist += [ildex[j], ildex[j+1], ildex[j+2]]
    return ilist    

if __name__ == '__main__':
    width = 1280
    height = 720

    translate_mat = Mat4.from_translation(vector=Vec3(x=0, y=0, z=0))
    # Render window.
    renderer = RenderWindow(width, height, "Hello Pyglet", resizable = True)   
    renderer.set_location(200, 200)

    # Keyboard/Mouse control. Not implemented yet.
    controller = Control(renderer)
    pyglet.gl.glClearColor(0.5,0.5,0.5,1)
    f = open("Free_rock/Free_rock.obj", 'r')
    vertexList = []
    vertexNormalList = []
    vertexTextureList = []
    indexListRaw = []
    indexVertexList = []
    indexNormalList = []
    indexTextureList = []
    indexList = []
    while True:
        offset = 1
        line = f.readline()
        token = line.split(' ')
        if len(token) > 3:
            if token[0] == 'v':
                vertexList += [float(token[1+offset]), float(token[2+offset]), float(token[3+offset])]
            elif token[0] == 'vn':
                vertexNormalList += [float(token[1]), float(token[2]), float(token[3])]
            elif token[0] == 'vt':
                vertexTextureList += [float(token[1]), float(token[2])]
            elif token[0] == 'f':
                for k in token[1:-1]:
                    index, texture, normal = tuple(map(lambda x: int(x)-1,k.split('/')))
                    indexListRaw.append(index)
                    indexVertexList += vertexList[3*index:3*index+3]
                    indexTextureList += vertexTextureList[2*texture:2*texture+2]
                    indexNormalList += vertexNormalList[3*normal:3*normal+3]
        if line == 'END':
            break
    f.close()
    indexListLine = ctwo(indexListRaw, 3)
    indexListFace = list(range(len(indexVertexList)))
    renderer.add_polygon(translate_mat, indexListFace, indexNormalList, indexVertexList, indexTextureList)
    renderer.add_wire(translate_mat, indexListLine, vertexList)

    #draw shapes
    renderer.run()
