from gl import Render
from vector import V3


def glpoint():
    r = Render()
    r.glCreateWindow(500,500)

    r.glClearColor(0.52,0.81,0.92) #parametros en rango de 0 a 1
    r.glClear()

    r.glViewPort(0,0,500,500) 

    r.glColor(1,1,1) #parametros en rango de 0 a 1

    ''' PLANTA 3D'''
    r.glLoad('./tree.obj', (0,-0.2,0), (0.3,0.3,0.3))
    
    #out.bmp retorna render del modelo usando flat shading
    r.glFinish()

    ''' render zbuffer'''
    r.glFinishZbuffer()
    #zbuffer.bmp retorna render del zbuffer

glpoint()


# Correr python3 main.py para ejecutar el programa. 
# Se tarda unos 3-4 minutos en renderizar, pero creo que es cosa de mi compu.

