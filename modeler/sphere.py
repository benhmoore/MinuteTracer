from modeler.world_object import WorldObject

class Sphere(WorldObject):

    def __init__(self, radius:float, position:tuple[float], color:tuple[float], specular:int=-1):
        self.radius = radius
        self.position = position
        self.color = color
        self.specular = specular