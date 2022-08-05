# ===============================================================
# Gráficas Por Computadora
# Stefano Aragoni - 20261
# ===============================================================

from logging import raiseExceptions
import struct

# ========== Tamaños =========

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  return struct.pack('=h', w)

def dword(d):
  return struct.pack('=l', d)

def color(r, g, b):
  return bytes([int(b*255), int(g*255), int(r*255)])

# ========== Colores =========

BLACK = color(0, 0, 0)
WHITE = color(1, 1, 1)

# ========== Render =========

class Render(object):
  def __init__(self):
    self.current_color = BLACK
    self.background_color = WHITE

  def glCreateWindow(self, width=100, height=100):
    self.width = width
    self.height = height
    self.inc = 1/height

  def glViewPort(self, x=0, y=0, width=99, height=99):
    self.width2 = width-1
    self.height2 = height-1
    self.x2 = x
    self.y2 = y

  def glClear(self):
    self.pixels = [
      [self.background_color for x in range(self.width)] 
      for y in range(self.height)
    ]

  def glColor(self, r, g, b):
    if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
      raise Exception('Color RGB invalido. Ingrese valores entre 0 y 1.')

    self.current_color = color(r, g, b)

  def glClearColor(self, r, g, b):
    if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
      raise Exception('Color RGB invalido. Ingrese valores entre 0 y 1.')
    self.background_color = color(r, g, b)

  def glFinish(self):
    f = open('out.bmp', 'bw')

    # File header (14 bytes)
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    # Image header (40 bytes)
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    for y in range(self.height-1, -1, -1):
      for x in range(self.width):
        f.write(self.pixels[x][y])

    f.close()

  def glVertex(self, x, y):
    if not (-1 <= x <= 1) or not (-1 <= y <= 1):
      raise Exception('Coordenada invalida. Ingrese valores entre -1 y 1.')

    try:
      X0 = int(self.x2 + (self.width2/2) + (x * self.width2/2))
      Y0 = int(self.y2 + (self.height2/2) + (-y * self.height2/2))
      self.pixels[X0][Y0] = self.current_color
      
    except:
      pass

  def glLine(self, x0, y0, x1, y1):

    if not (-1 <= x0 <= 1) or not (-1 <= y0 <= 1) or not (-1 <= x1 <= 1) or not (-1 <= y1 <= 1):
      raise Exception('Coordenada invalida. Ingrese valores entre -1 y 1.')
        
    pendiente = abs(y1 - y0) > abs(x1 - x0) 

    if (pendiente):
      x0, y0 = y0, x0
      x1, y1 = y1, x1

    if x0 > x1:
      x0, x1 = x1, x0
      y0, y1 = y1, y0

    dy, dx = abs(y1 - y0), abs(x1 - x0)
    y, x = y0, x0

    offdy, offdx = 0, dx

    while (x < x1):
      offdy += dy * 2

      #creacion de puntos
      if pendiente:
        self.glVertex(y, x)
      else:
        self.glVertex(x, y)

      #incrementa/reduce Y conforme pasitos proporcionales
      if offdy >= offdx:
        if y < y1:
          y += self.inc #self.inc se calcula al crear el Window
        else:
          y -= self.inc
          
        offdx += dx * 2
      
      #incrementa X conforme pasitos proporcionales
      x += self.inc


  def glLoad(self, filename, translate, scale):
    archivo = Obj(filename)
    
    for face in archivo.faces:
      vcount = len(face)

      for j in range(vcount):
        v1 = archivo.vertex[(face[j][0]) - 1]
        v2 = archivo.vertex[(face[(j + 1) % vcount][0]) - 1]
        
        x1 = ((v1[0] + translate[0]) * scale[0])
        y1 = ((v1[1] + translate[1]) * scale[1])
        x2 = ((v2[0] + translate[0]) * scale[0])
        y2 = ((v2[1] + translate[1]) * scale[1])

        self.glLine(x1, y1, x2, y2)


class Obj(object):
  def __init__(self, filename):
    with open(filename) as f:
      self.lines = f.read().splitlines()

    self.vertex = []  #v
    self.faces = [] #f

    for line in self.lines:
      if line:
        prefix, value = line.split(' ', 1)

        if prefix == 'v':
          temp = value.split(' ')
          tempArray = []

          for tempValue in temp:
            tempArray.append((float(tempValue)))

          self.vertex.append(tempArray)

          
        elif prefix == 'f':
          temp = value.split(' ')
          tempArray = []
          
          for tempValue in temp:
            temp2 = tempValue.split('/')
            tempArray2 = []

            for tempValue2 in temp2:
              tempArray2.append((int(tempValue2)))

            tempArray.append(tempArray2)
          
          self.faces.append(tempArray)

