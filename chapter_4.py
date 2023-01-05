from renderer import Renderer
from modeler import World
from modeler import *

my_world = World(ppu=256)

# Spheres
my_world.addObject(Sphere(1, (0,-1,3), (255,0,0), 500, 0.2))
my_world.addObject(Sphere(1, (2,0,4), (0,0,255), 500, 0.3))
my_world.addObject(Sphere(1, (-2,0,4), (0,255,0), 10, 0.4))
my_world.addObject(Sphere(5000, (0,-5001,0), (255,255,0), 1000, 0.5))

# Lights
my_world.addObject(AmbientLight(0.2))
my_world.addObject(PointLight(0.6,(2,1,0)))
my_world.addObject(DirectionalLight(0.2,(1,4,4)))

r_t = Renderer(my_world, pixel_dimensions=(256,256))

frame_img = r_t.render()
frame_img.save("img/chapter_4.png")