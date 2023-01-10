from renderer import Renderer
from modeler import *

poly_world = World(ppu=100)

# Load mesh from file
m = Mesh("mesh/mesh-export.csv", (0, 50, 255), 0.9,0.75)
poly_world.addObject(m)

# Add sphere
poly_world.addObject(Sphere(0.3, (-0.2, 0.4, 2), (20, 255, 20), 2, 0.85))
poly_world.addObject(Sphere(0.3, (0.4, -0.5, 0.5), (255, 20, 20), 2, 0.85))
poly_world.addObject(Sphere(0.1, (-0.4, -0.8, 1.2), (254, 224, 71), 2, 0.85))

# Add lights
poly_world.addObject(AmbientLight(0.1))
poly_world.addObject(PointLight(3,(1,8,-5)))
poly_world.addObject(PointLight(0.5,(1,-4,5)))

r_t = Renderer(poly_world, pixel_dimensions=(100,100))

r_t.setCameraPosition((0, 0, -1))
frame_img = r_t.render()
frame_img.save("img/meshes.png")