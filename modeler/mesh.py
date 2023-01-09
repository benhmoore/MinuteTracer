from modeler.world_object import WorldObject
from modeler.triangle import Triangle
from lib.mesh_utils import loadMeshFile

class Mesh(WorldObject):

    CO = None
    c = None

    def __init__(self, mesh_file:str, color:tuple[float], specular:int=-1, reflective:float=0.0):

        self.color = color
        self.specular = specular
        self.reflective = reflective

        self.mesh_triangles = loadMeshFile(mesh_file)
        self.triangles = []
        for tri in self.mesh_triangles:
            self.triangles.append(Triangle((tri[0], tri[1], tri[2]), self.color, self.specular, self.reflective))