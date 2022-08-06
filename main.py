from gl import Render
from vector import V3


def glpoint():
    r = Render()
    r.glCreateWindow(1000,1000)

    r.glClearColor(0,0,0) #parametros en rango de 0 a 1
    r.glClear()

    r.glViewPort(0,0,1000,1000) 

    r.glColor(1,1,1) #parametros en rango de 0 a 1

    r.glLoad('./mario.obj', (0,-0.5,0), (0.013,0.013,0.013))

    r.triangle(0.01, 0.07, 0.05, 0.16, 0.07, 0.08)

    r.glFinish()

glpoint()



