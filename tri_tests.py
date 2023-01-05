from renderer import Renderer
from modeler import *

poly_world = World(ppu=1024)

# Background Spheres
poly_world.addObject(Sphere(.3, (0.35, 0, 1.8), (255, 150, 64), 100, 0.3))
poly_world.addObject(Sphere(.3, (-0.35, 0, 1.8), (100, 100, 255), 100, 0.3))
# poly_world.addObject(Sphere(.1, (-.3, 0, 3), (200, 150, 64)))
# poly_world.addObject(Sphere(.1, (0, -0.3, 2), (100, 150, 64)))

# # First poly!
a1 = (0, 0.5, 2)
a2 = (0.001, 0.501, 2.001)
b1 = (-0.3, 0, 3)
b2 = (0.3, 0, 3)
c1 = (0, -0.3, 1)
c2 = (0.001, -0.3001, 2.001)

poly_world.addObject(Triangle((a1, b1, c1),(0,255,0), 100, 0.3))
poly_world.addObject(Triangle((a2, b2, c2),(0,255,0), 100, 0.3))


# # Second poly!
# a = (1, 0, 5)
# b = (1, 1, 5)
# c = (-2, 0.5, 12)

# poly_world.addObject(Triangle((a, b, c),(0,255,0), 1, 0.1))


# Lights
poly_world.addObject(AmbientLight(0.2))
poly_world.addObject(PointLight(0.9,(-2,5,4)))
poly_world.addObject(DirectionalLight(0.2,(1,4,4)))

r_t = Renderer(poly_world, pixel_dimensions=(1024,1024))

r_t.setCameraPosition((0,0.0,0))


frame_img = r_t.render()
frame_img.save("tri_tests.png")
# print(poly_world.objects[0].normal_vec)