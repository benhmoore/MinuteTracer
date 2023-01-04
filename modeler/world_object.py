class WorldObject:

    position:tuple[float]  = (0,0,0)
    direction:tuple[float] = (0,0,0)
    radius:float           = 0
    color:tuple[float]     = (0,0,0)
    specular:int           = -1
    reflective:float       = 0.0
    
    def __init__(self, position):
        self.position = position