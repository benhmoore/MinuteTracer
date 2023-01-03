from renderer import Renderer
from modeler import World
from modeler import Sphere

my_world = World(ppu=512)

my_world.addObject(Sphere(1.1, (1,1,5), (238,120,47)))
my_world.addObject(Sphere(2, (-2,-2,5), (229,228,75)))

r_t = Renderer(my_world, pixel_dimensions=(512,512))

frame_img = r_t.render()
frame_img.save("balls.png")