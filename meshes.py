from renderer import Renderer
from modeler import *

poly_world = World(ppu=256)

# Load mesh from file
m = Mesh("mesh/mesh-export.csv", (0, 50, 255), 1000,0.7)
poly_world.addObject(m)

# Add sphere
poly_world.addObject(Sphere(0.5, (0, 0, 0.8), (20, 255, 20), 1000, 0.4))

# Add lights
poly_world.addObject(AmbientLight(0.1))
poly_world.addObject(PointLight(3,(1,4,-1)))

r_t = Renderer(poly_world, pixel_dimensions=(256,256))

r_t.setCameraPosition((0, 0, -1.5))
frame_img = r_t.render()
frame_img.save("img/meshes.png")