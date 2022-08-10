from gl import Render

def glpoint():
    r = Render()
    r.glCreateWindow(500,500)

    r.glClearColor(0.35,0.35,0.35) #parametros en rango de 0 a 1
    r.glClear()

    r.glViewPort(0,0,500,500) 

    r.glColor(1,1,1) #parametros en rango de 0 a 1

    ''' CARRO 3D'''
    r.glLoad('./Car.obj', (0,-200,0), (300,300,300))
    
    #out.bmp retorna render del modelo usando flat shading
    r.glFinish()

    ''' render zbuffer'''
    r.glFinishZbuffer()
    #zbuffer.bmp retorna render del zbuffer

glpoint()


# Correr python3 main.py para ejecutar el programa. 