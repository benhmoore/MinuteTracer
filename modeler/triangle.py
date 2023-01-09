from lib import math_functions
from modeler.world_object import WorldObject


class Triangle(WorldObject):

    def __init__(self, points:tuple[tuple], color:tuple[float], specular:int=-1, reflective:float=0.0):
        self.points = points
        self.color = color
        self.specular = specular
        self.reflective = reflective

        # Calculate normal of triangle
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]

        # Compute the normal of the plane that contains the triangle
        p1p2 = math_functions._subtractVec(p2, p1)
        p1p3 = math_functions._subtractVec(p3, p1)

        self.normal_vec = math_functions._crossProduct(p1p2, p1p3)
        # needs to be inverted