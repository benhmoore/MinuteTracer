from modeler.world_object import *
from modeler.light import *

class World(WorldObject):
    def __init__(self, ppu:int=16, unit:str="cm"):
        """World Initializer.
        Args:
            ppu (int, optional): Pixels per unit. Describes the number of pixels per unit vector. Defaults to 16.
            unit (str, optional): Human-readable description of unit. Defaults to "cm".
        """        
        self.unit = unit
        self.scale = ppu
        self.objects:list[WorldObject] = []

    
    def addObject(self, world_object: WorldObject):
        self.objects.append(world_object)

    def getLights(self):
        lights = []
        for world_obj in self.objects:
            if isinstance(world_obj, Light):
                lights.append(world_obj)
                
        return lights


world = World()

