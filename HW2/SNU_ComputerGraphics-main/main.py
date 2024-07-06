import pyglet
from pyglet.math import Mat4, Vec3, Vec4

from render import *
from primitives import Cube,Sphere
from control import Control
from tkinter import *




    

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
def catmull(vlist, ilist2, l):
    Fp = []
    Ep = []
    Bp = []
     # Face Point & Boundary
    for i in range(int(len(ilist2)/l)):
        faceIx = ilist2[i*l:(i+1)*l]
        newV = [0,0,0]
        newE = [0,0,0]
        for j in faceIx:
            newV[0] += vlist[3*j] / l
            newV[1] += vlist[3*j+1] / l
            newV[2] += vlist[3*j+2] / l
        Fp += newV
    # Interior edge Point
    for i in range(int(len(ilist2)/l)):
        for j in range(i+1, int(len(ilist2)/l)):
            faceIxA = ilist2[i*l:(i+1)*l]
            faceIxB = ilist2[j*l:(j+1)*l]
            vx = (-1,-1)
            for ai in range(-1,l-1):
                for bj in range(-1, l-1):
                    if (faceIxA[ai], faceIxA[ai+1]) == (faceIxB[bj], faceIxB[bj+1]) or (faceIxA[ai], faceIxA[ai+1]) == (faceIxB[bj+1], faceIxB[bj]):
                        vx = (faceIxA[ai],  faceIxA[ai+1])
                        newV = [0,0,0]
                        newV[0] += vlist[3*vx[0]]
                        newV[1] += vlist[3*vx[0]+1]
                        newV[2] += vlist[3*vx[0]+2]
                        newV[0] += vlist[3*vx[1]]
                        newV[1] += vlist[3*vx[1]+1]
                        newV[2] += vlist[3*vx[1]+2]
                        newV[0] += Fp[3*i]
                        newV[1] += Fp[3*i+1]
                        newV[2] += Fp[3*i+2]
                        newV[0] += Fp[3*j]
                        newV[1] += Fp[3*j+1]
                        newV[2] += Fp[3*j+2]
                        newV[0] /= l
                        newV[1] /= l
                        newV[2] /= l
                        Ep += newV
                        Bp.append(vx)
    # step3
    for i in range(int(len(vlist)/3)):
        idlst = []
        mycoor = vlist[3*i:3*(i+1)]
        newp = [0,0,0]
        for j in range(len(ilist2)):
            if i == ilist2[j]:
                idlst.append(j)
        n = len(idlst)
        if n == 1:
            id1 = ilist2[(idlst[0]//4)*l-1]
            id2 = ilist2[(idlst[0]//4)*l+1]
            newp[0] = (vlist[id1*3] + vlist[id2*3] + 6*mycoor[0]) / 8
            newp[1] = (vlist[id1*3+1] + vlist[id2*3+1] + 6*mycoor[1]) / 8
            newp[2] = (vlist[id1*3+2] + vlist[id2*3+2] + 6*mycoor[2]) / 8
            vlist[3*i] = newp[0]
            vlist[3*i+1] = newp[1]
            vlist[3*i+2] = newp[2]
        else:
            f=[0,0,0]
            r=[]
            rc=[0,0,0]
            for ts in idlst:
                f[0] += Fp[(ts//4)*3]
                f[1] += Fp[(ts//4)*3+1]
                f[2] += Fp[(ts//4)*3+2]
            for bm in range(len(Bp)):
                aj, ab = Bp[bm]
                if aj == i or ab == i:
                    rc[0] += Ep[3*bm]
                    rc[1] += Ep[3*bm+1]
                    rc[2] += Ep[3*bm+2]
            rc[0] /= n
            rc[1] /= n
            rc[2] /= n
            f[0] /= n
            f[1] /= n
            f[2] /= n
            newp[0] = (f[0] + 2*rc[0] + (n-3)*mycoor[0]) / n
            newp[1] = (f[1] + 2*rc[1] + (n-3)*mycoor[1]) / n
            newp[2] = (f[2] + 2*rc[2] + (n-3)*mycoor[2]) / n
            vlist[3*i] = newp[0]
            vlist[3*i+1] = newp[1]
            vlist[3*i+2] = newp[2]
    # step 4
    pn = int(len(vlist)/3)
    vlist += Ep
    fpn = int(len(vlist)/3)
    newlst = []
    k = 0
    for i in range(int(len(ilist2)/l)):
        faceIx = ilist2[i*l:(i+1)*l]
        vlist += Fp[3*i:3*i+3]
        fpn += 1
        for j in faceIx:
            for bm in range(len(Bp)):
                for gs in range(bm+1, len(Bp)):
                    aj, ab = Bp[bm]
                    pb, gp = Bp[gs]
                    if aj in faceIx and ab in faceIx and pb in faceIx and gp in faceIx:
                        if aj == j and pb == j or ab == j and pb == j or aj == j and gp == j or ab == j and gp == j:
                            k += 1
                            newlst.append(j)
                            newlst.append(bm+pn)
                            newlst.append(fpn-1)
                            newlst.append(gs+pn)
    return (vlist, newlst)
if __name__ == '__main__':
    width = 1280
    height = 720

    # Render window.
    tk = Tk()
    l1 = Label(tk, text = "Welcome to Spline/Subdivision Simulator", )
    l2 = Label(tk, text = "Push the button to start simulation")
    radiomode = IntVar()
    r1 = Radiobutton(tk, text="Grid / Bezier Curve", variable=radiomode, value = 0)
    r2 = Radiobutton(tk, text="Grid / B Spline", variable=radiomode, value = 1)
    r3 = Radiobutton(tk, text="Cross Cube / Subdivision", variable=radiomode, value = 2)
    r4 = Radiobutton(tk, text="Icosahedron / Subdivision", variable=radiomode, value = 3)
    rval = IntVar()
    gval = IntVar()
    bval = IntVar()
    l3 = Label(tk, text = "Polygon Color")
    l4 = Label(tk, text="R")
    l5 = Label(tk, text="G")
    l6 = Label(tk, text="B")
    red = Scale(tk, variable=rval, orient="horizontal", tickinterval=255, to=255, length=255, showvalue=True)
    green = Scale(tk, variable=gval, orient="horizontal", tickinterval=255, to=255, length=255, showvalue=True)
    blue = Scale(tk, variable=bval, orient="horizontal", tickinterval=255, to=255, length=255, showvalue=True)
    but = Button(tk, text="Start", command=(lambda *args : tk.destroy()))
    tk.protocol('WM_DELETE_WINDOW', (lambda *args : exit(1)))
    l1.pack()
    l2.pack()
    r1.pack()
    r2.pack()
    r3.pack()
    r4.pack()
    l3.pack()
    l4.pack()
    red.pack()
    l5.pack()
    green.pack()
    l6.pack()
    blue.pack()
    but.pack()

    tk.mainloop()
    nunez = radiomode.get()

    if nunez == 0:
        f = open('SurfaceMesh/Spline/grid.obj', 'r')
        SUB = 0
        MODE = 1
    elif nunez == 1:
        f = open('SurfaceMesh/Spline/grid.obj', 'r')
        SUB = 0
        MODE = 0
    elif nunez == 2:
        f = open('SurfaceMesh/Subdivision/cross_cube.obj', 'r')
        SUB = 1
        MODE = 0
    else:
        f = open('SurfaceMesh/Subdivision/icosahedron.obj', 'r')
        SUB = 1
        MODE = 0
    savefile = open('Result.obj', 'w')
    renderer = RenderWindow(width, height, "Hello Pyglet", resizable = True)
    renderer.modset(MODE)
    renderer.colorset(rval.get(), gval.get(), bval.get())
    renderer.set_location(200, 200)
    pyglet.gl.glClearColor(0.5,0.5,0.5,1)


    # Keyboard/Mouse control. Not implemented yet.
    controller = Control(renderer)
    controller.sset(nunez)
    translate_mat = Mat4.from_translation(vector=Vec3(x=0, y=0, z=0))

    # Making Control Points
    vlist = []
    ilist = []
    ilist2 = []
    while True:
        line = f.readline()
        tk = line.split(' ')
        if tk[0] != 'v':
            l = len(tk)-1
            for i in range(1,l+1):
                ilist2.append(int(tk[i])-1)
            break
        else:
            vlist += [float(tk[1]), float(tk[2]), float(tk[3][:-1])]
    while True:
        line = f.readline()
        tk = line.split(' ')
        if tk[0] != 'f':
            break
        else:
            for i in range(1,l+1):
                ilist2.append(int(tk[i])-1)
    f.close()
    ilist = ctwo(ilist2, l)
    renderer.add_polygon(translate_mat, ilist, vlist, True)
    
    if SUB:
        for i in range(STEP):
            vlist, ilist2 = catmull(vlist, ilist2, l)
            l = 4
        
        ilist = ctwo(ilist2, l)
        ilistS = cth(ilist2, l)
        ww = intotxt(ilist2, vlist, l)
        savefile.write(ww)
        savefile.close()
        renderer.add_polygon(translate_mat, ilistS, vlist, False)
        renderer.add_polygon(translate_mat, ilist, vlist, True)

    else:
        ilist = ctwo(ilist2, l)
        # Making Spline Matrix
        xt = []
        yt = []
        zt = []
        for i in range(int(len(vlist)/3)):
            xt.append(vlist[3*i])
            yt.append(vlist[3*i+1])
            zt.append(vlist[3*i+2])
        
        if MODE:
            changeOfBasis = BEZIER_MATRIX
            changeOfBasisT = BEZIER_TRANS
        else:
            changeOfBasis = BSPLINE_MATRIX
            changeOfBasisT = BSPLINE_TRANS    
        matX = changeOfBasisT @ Mat4(xt) @ changeOfBasis
        matY = changeOfBasisT @ Mat4(yt) @ changeOfBasis
        matZ = changeOfBasisT @ Mat4(zt) @ changeOfBasis
        

        vlistS = []
        ilistS = []
        ilistN = []
        ilistP = []
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
                if i != SAMPLE-1 and j != SAMPLE-1:
                    ilistS += [SAMPLE*i+j, SAMPLE*i+j+1, SAMPLE*i+j+1+SAMPLE]
                    ilistS += [SAMPLE*i+j+1+SAMPLE,SAMPLE*i+j+SAMPLE, SAMPLE*i+j]

                    ilistN += [SAMPLE*i+j, SAMPLE*i+j+1]
                    ilistN += [SAMPLE*i+j+1, SAMPLE*i+j+SAMPLE+1]
                    ilistN += [SAMPLE*i+j+SAMPLE, SAMPLE*i+j+1+SAMPLE]
                    ilistN += [SAMPLE*i+j+SAMPLE, SAMPLE*i+j]
                    ilistP += [SAMPLE*i+j, SAMPLE*i+j+1, SAMPLE*i+j+SAMPLE+1, SAMPLE*i+j+SAMPLE]
        ww = intotxt(ilistP, vlistS, l)
        savefile.write(ww)
        savefile.close()
        renderer.add_polygon(translate_mat, ilistS, vlistS, False)
        renderer.add_polygon(translate_mat, ilistN, vlistS, True)

    #draw shapes
    renderer.run()
