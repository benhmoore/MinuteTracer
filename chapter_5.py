from renderer import Renderer
from modeler import World
from modeler import *

my_world = World(ppu=256)

# Spheres
my_world.addObject(Sphere(1, (0,-1,3), (255,0,0), 500, 0.8))
my_world.addObject(Sphere(1, (2,0,4), (0,0,255), 500, 0.8))
my_world.addObject(Sphere(1, (-2,0,4), (0,255,0), 500, 0.8))
my_world.addObject(Sphere(5000, (0,-5001,0), (150,150,150), 1000, 0.5))

# Lights
# my_world.addObject(AmbientLight(0))
my_world.addObject(PointLight(0.9,(2,1,0)))
my_world.addObject(DirectionalLight(0.2,(1,4,4)))

r_t = Renderer(my_world, pixel_dimensions=(256,256))

r_t.setCameraPosition((0,1,10))
r_t.setCameraRotation([
    [1, 0, 0],
    [0, 1, -.2],
    [0, 0, -1],
])

frame_img = r_t.render()
frame_img.save("img/chapter_5.png")