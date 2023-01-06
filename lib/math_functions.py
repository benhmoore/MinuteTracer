import math


_dot_product_cache = {}

def _dotProduct(a:tuple, b:tuple) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def _crossProduct(a:tuple, b:tuple) -> tuple[float]:
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    )

def _subtractVec(a:tuple, b:tuple) -> tuple[float]:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def _multiplyVec(k:float, vec:tuple) -> tuple[float]:
    return (k*vec[0], k*vec[1], k*vec[2])

def _multiplyMat(mat, vec):
    result_vec = [0, 0, 0]
    for i in range(0, 3):
        for j in range(0, 3):
            result_vec[i] += vec[j] * mat[i][j]
    
    return tuple(result_vec)

def _addVec(a:tuple, b:tuple) -> tuple[float]:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def _reflectVec(v1:tuple, v2:tuple) -> tuple[float]:
    return _subtractVec(_multiplyVec(2.0 * _dotProduct(v2, v1), v2), v1)

def _lengthVec(a:tuple) -> float:
    return math.sqrt(_dotProduct(a, a))

def _clampColorVec(color_vec) -> tuple[int]:
    """Clamps a color vector to integer values between 0 and 255.
    """
    return (
            int(min(255, max(0, color_vec[0]))),
            int(min(255, max(0, color_vec[1]))),
            int(min(255, max(0, color_vec[2]))),
        )