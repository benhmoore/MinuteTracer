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
        self.p1p2 = math_functions._subtractVec(p2, p1)
        self.p1p3 = math_functions._subtractVec(p3, p1)

        self.p2p3 = math_functions._subtractVec(p3, p2)
        self.p3p1 = math_functions._subtractVec(p1, p3)

        self.normal_vec = math_functions._crossProduct(self.p1p2, self.p1p3)

        # Compute d
        self.d = math_functions._dotProduct(self.normal_vec, p1)

        self.ray_origin = None
        self.normal_dot_origin = None
