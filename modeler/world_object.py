class WorldObject:

    position:tuple[float]  = (0,0,0)
    direction:tuple[float] = (0,0,0)
    radius:float           = 0
    color:tuple[float]     = (0,0,0)
    specular:int           = -1
    reflective:float       = 0.0
    points:tuple[tuple]    = None

    def _dotProduct(self, a:tuple, b:tuple) -> float:
        return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


    def _crossProduct(self, a:tuple, b:tuple) -> tuple[float]:
        return ( 
            a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]
        )

    def _subtractVec(self, a:tuple, b:tuple) -> tuple[float]:
        return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
    
    def _multiplyVec(self, k:float, vec:tuple) -> tuple[float]:
        return (k*vec[0], k*vec[1], k*vec[2])

    def _multiplyMat(self, mat, vec):
        result_vec = [0, 0, 0]
        for i in range(0, 3):
            for j in range(0, 3):
                result_vec[i] += vec[j] * mat[i][j]
        
        return tuple(result_vec)

    def _addVec(self, a:tuple, b:tuple) -> tuple[float]:
        return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

    def _reflectVec(self, v1:tuple, v2:tuple) -> tuple[float]:
        return self._subtractVec(self._multiplyVec(2.0 * self._dotProduct(v2, v1), v2), v1)

    def _lengthVec(self, a:tuple) -> float:
        return math.sqrt(self._dotProduct(a, a))
    
    def __init__(self, position):
        self.position = position