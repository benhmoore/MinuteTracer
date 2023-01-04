from modeler.world_object import WorldObject

class Light(WorldObject):
    def __init__(self):
        self.intensity = 0
        self.position = (0,0,0)
        self.direction = (0,0,0)

class AmbientLight(Light):
    def __init__(self, intensity:float):
        super().__init__()
        self.intensity = intensity

class PointLight(Light):
    def __init__(self, intensity:float, position:tuple[float]):
        super().__init__()
        self.intensity = intensity
        self.position = position

class DirectionalLight(Light):
    def __init__(self, intensity:float, direction:tuple[float]):
        super().__init__()
        self.intensity = intensity
        self.direction = direction