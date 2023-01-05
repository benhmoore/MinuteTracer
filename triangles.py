from renderer import Renderer
from modeler import *

poly_world = World(ppu=256)

# Define gem made of two triangles
a = (-0.05, 0.5, 1.1)
b1 = (-0.3, 0, 2)
b2 = (0.3, 0, 2)
c = (0.05, -0.3, 1.1)

# # normal should be inverted
poly_world.addObject(Triangle((a, b1, c),(255,255,0), 500, 0.4))

# # normal calculation correct
poly_world.addObject(Triangle((a, b2, c),(255,255,0),500, 0.4))

# Spheres
poly_world.addObject(Sphere(1, (0,-1,3), (255,0,0), 500, 0.2))
poly_world.addObject(Sphere(1, (2,0,4), (0,0,255), 500, 0.3))
poly_world.addObject(Sphere(1, (-2,0,4), (0,255,0), 10, 0.4))
poly_world.addObject(Sphere(5000, (0,-5001,0), (255,255,0), 1000, 0.5))

# Lights
poly_world.addObject(AmbientLight(0.2))
poly_world.addObject(PointLight(0.6,(2,1,0)))
poly_world.addObject(DirectionalLight(0.2,(1,4,4)))



r_t = Renderer(poly_world, pixel_dimensions=(256,256))

# r_t.setCameraPosition((0,0.0,0))


frame_img = r_t.render()
frame_img.save("img/triangles.png")
# print(poly_world.objects[0].normal_vec)