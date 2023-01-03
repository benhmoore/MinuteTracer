from modeler.world_object import WorldObject

class Sphere(WorldObject):

    def __init__(self, radius:float, position:tuple[float], color:tuple[float]):
        self.radius = radius
        self.position = position
        self.color = color