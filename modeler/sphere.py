from modeler.world_object import WorldObject

class Sphere(WorldObject):

    CO = None
    c = None

    def __init__(self, radius:float, position:tuple[float], color:tuple[float], specular:int=-1, reflective:float=0.0):
        self.radius = radius
        self.radius_sq = radius**2
        self.position = position
        self.color = color
        self.specular = specular
        self.reflective = reflective