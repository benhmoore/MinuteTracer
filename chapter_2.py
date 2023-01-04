from renderer import Renderer
from modeler import World
from modeler import *

my_world = World(ppu=512)

my_world.addObject(Sphere(1, (0,-1,3), (255,0,0)))
my_world.addObject(Sphere(1, (2,0,4), (0,0,255)))
my_world.addObject(Sphere(1, (-2,0,4), (0,255,0)))

r_t = Renderer(my_world, pixel_dimensions=(512,512))

frame_img = r_t.render()
frame_img.save("chapter_2.png")