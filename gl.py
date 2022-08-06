# ===============================================================
# Gráficas Por Computadora
# Stefano Aragoni - 20261
# ===============================================================

from logging import raiseExceptions
import struct
import random
from vector import V3
from vector import *

# ========== Tamaños =========

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  return struct.pack('=h', w)

def dword(d):
  return struct.pack('=l', d)

def color(r, g, b):
  return bytes([int(b*255), int(g*255), int(r*255)])


# ========== Utils =========

def bounding_box(x1, y1, x2, y2, x3, y3):
  coords = [(x1,y1),(x2,y2),(x3,y3)]

  xs = [x1, x2, x3]
  xs.sort()
  ys = [y1, y2, y3]
  ys.sort()

  return V3(xs[0], ys[0]), V3(xs[-1], ys[-1])

def barycentric(x1, y1, x2, y2, x3, y3, x4, y4):

  c = V3.cross(
    V3(x2 - x1, x3 - x1, x1 - x4), 
    V3(y2 - y1, y3 - y1, y1 - y4)
  )

  if c.z == 0:
    return -1, -1, -1

  u = c.x / c.z
  v = c.y / c.z
  w = 1 - (c.x + c.y) / c.z

  return (w,v,u)

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

    self.zbuffer = [
			[-99999 for x in range(self.width)]
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

  def triangle(self, x1, y1, x2, y2, x3, y3, z1=0, z2=0, z3=0, color=None):

    min, max = bounding_box(x1, y1, x2, y2, x3, y3)

    while((min.x) < (max.x) + 1):
      temp = min.y
      while((temp) < (max.y) + 1):
        w, v, u = barycentric(x1, y1, x2, y2, x3, y3, min.x, temp)

        if w < 0 or v < 0 or u < 0: 
          temp = temp + self.inc
          continue

        z = z1 * w + z2 * v + z3 * u
        try:
          if z > self.zbuffer[int(min.x*self.width)][int(temp*self.height)]:
            self.current_color = color
            self.glVertex(min.x, temp)
            self.zbuffer[int(min.x*self.width)][int(temp*self.height)] = z
        except:
          pass

        temp = temp + self.inc
      min.x = min.x + self.inc


  def transform_vertex(self, vertex, scale, translate):
    return V3(
      (vertex[0] * scale[0] + translate[0]),
      (vertex[1] * scale[1] + translate[1]),
      (vertex[2] * scale[2] + translate[2]),
    )
    
  def glLoad(self, filename, translate=(0,0,0), scale=(1,1,1)):
    archivo = Obj(filename)
    light = V3(0,0,1)
    
    for face in archivo.faces:
      vcount = len(face)

      if vcount == 3:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1

        v1 = self.transform_vertex(archivo.vertex[f1], scale, translate)
        v2 = self.transform_vertex(archivo.vertex[f2], scale, translate)
        v3 = self.transform_vertex(archivo.vertex[f3], scale, translate)

        normal = V3.normalize(V3.cross(V3.__sub__(v2, v1), V3.__sub__(v3, v1)))

        intensity = V3.dot(normal, light)
        if intensity < 0:
          continue  
				
        self.triangle(v1.x, v1.y, v2.x, v2.y, v3.x, v3.y, v1.z, v2.z, v3.z, color(intensity, intensity, intensity))

      if vcount == 4:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1
        f4 = face[3][0] - 1

        v1 = self.transform_vertex(archivo.vertex[f1], scale, translate)
        v2 = self.transform_vertex(archivo.vertex[f2], scale, translate)
        v3 = self.transform_vertex(archivo.vertex[f3], scale, translate)
        v4 = self.transform_vertex(archivo.vertex[f4], scale, translate)

        normal = V3.normalize(V3.cross(V3.__sub__(v1, v2), V3.__sub__(v2, v3)))
        intensity = V3.dot(normal, light)
        if intensity < 0:
          continue  
        
        self.glLine(v1.x, v1.y, v2.x, v2.y)
        self.glLine(v2.x, v2.y, v3.x, v3.y)
        self.glLine(v3.x, v3.y, v4.x, v4.y)
        self.glLine(v4.x, v4.y, v1.x, v1.y)

        self.triangle(v1.x, v1.y, v2.x, v2.y, v3.x, v3.y, v1.z, v2.z, v3.z, color(intensity, intensity, intensity))
        self.triangle(v1.x, v1.y, v4.x, v4.y, v3.x, v3.y, v1.z, v4.z, v3.z, color(intensity, intensity, intensity))


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
  