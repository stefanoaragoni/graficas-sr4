from gl import Render


def glpoint():
    r = Render()
    r.glCreateWindow(1000,1000)

    r.glClearColor(0.15,0,0.5) #parametros en rango de 0 a 1
    r.glClear()

    r.glViewPort(0,0,1000,1000) 

    r.glColor(0.8,0.1,0.9) #parametros en rango de 0 a 1

    r.glLoad('./mario.obj', (0,-0.5,0), (0.013,0.013,0.013))

    r.glFinish()

glpoint()



