from gl import Render
from vector import V3


def glpoint():
    r = Render()
    r.glCreateWindow(500,500)

    r.glClearColor(1,1,1) #parametros en rango de 0 a 1
    r.glClear()

    r.glViewPort(0,0,500,500) 

    r.glColor(0,0,0) #parametros en rango de 0 a 1

    r.glLoad('./face.obj', (0,-0.5,0), (0.05,0.05,0.05))

    #r.triangle(0.1, 0.1, 0.2, 0.2, 0.3, 0.1)

    r.glFinish()

glpoint()



