from PIL import Image, ImageDraw
import math

import time

EPSILON = 0.000001

class Renderer:

    def __init__(self, world, pixel_dimensions:tuple, background_color:tuple=(0,0,0)):
        self.world = world
        self.width, self.height = pixel_dimensions
        self.background_color = background_color

        self.camera_rotation = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        self.camera_position = (0, 0, 0)
        
        self.d = 1 # Initialize distance between camera and viewport to 1

    def _canvasToViewport(self, x:int, y:int) -> tuple[float]:
        # Shorthand labels for canvas width and height
        c_w = self.width
        c_h = self.height

        # Calculate the size of the viewport by dividing the renderer's canvas by the scale of the world
        v_w = self.width / self.world.scale
        v_h = self.height / self.world.scale

        return (x*v_w/c_w, y*v_h/c_h, self.d)

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

    def _clampColorVec(self, color_vec) -> tuple[int]:
        """Clamps a color vector to integer values between 0 and 255.
        """
        return (
                int(min(255, max(0, color_vec[0]))),
                int(min(255, max(0, color_vec[1]))),
                int(min(255, max(0, color_vec[2]))),
            )

    def _computeLighting(self, point, normal_vec, view_vec, specular):
        intensity = 0.0
        length_normal = self._lengthVec(normal_vec)
        length_view = self._lengthVec(view_vec)

        if len(self.world.getLights()) < 1:
            return 1.0

        for light in self.world.getLights():
            if light.__class__.__name__ == 'AmbientLight':
                intensity += light.intensity
            else:
                if light.__class__.__name__ == 'PointLight':
                    L = self._subtractVec(light.position, point)
                    t_max = 1.0 - EPSILON
                else:
                    L = light.direction
                    t_max = math.inf

                # Shadow check
                shadow_sphere, shadow_t = self._calculateClosestIntersection(point, L, EPSILON, t_max)
                if shadow_sphere:
                    continue

                if self._dotProduct(normal_vec, L) < 0 and self._dotProduct(normal_vec, view_vec) < 0:
                    normal_vec = self._multiplyVec(-1, normal_vec)
                elif self._dotProduct(normal_vec, L) > 0 and self._dotProduct(normal_vec, view_vec) < 0:
                    normal_vec = self._multiplyVec(-1, normal_vec)

                # Diffuse
                normal_dot_L = self._dotProduct(normal_vec, L)
                

                if normal_dot_L > 0:
                    intensity += (light.intensity * normal_dot_L) / (length_normal * self._lengthVec(L))
        
                    # Specular
                    if specular != -1:
                        R_vec = self._reflectVec(L, normal_vec)
                        R_dot_V = self._dotProduct(R_vec, view_vec)
                        if R_dot_V > 0:
                            intensity += light.intensity * math.pow(R_dot_V / (self._lengthVec(R_vec) * length_view), specular)
        return intensity

    def _intersectRaySphere(self, origin, direction_vec, sphere):
        
        # Hardcoded to assume all objects are spheres
        CO = self._subtractVec(origin, sphere.position)

        a = self._dotProduct(direction_vec, direction_vec)
        b = 2 * self._dotProduct(CO, direction_vec)
        c = self._dotProduct(CO, CO) - sphere.radius**2

        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return math.inf, math.inf
        
        t_1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t_2 = (-b - math.sqrt(discriminant)) / (2 * a)

        return t_1, t_2

    def _intersectRayTriangle(self, origin, direction_vec, triangle):

        p1 = triangle.points[0]
        p2 = triangle.points[1]
        p3 = triangle.points[2]

        # Compute the normal of the plane that contains the triangle
        p1p2 = self._subtractVec(p2, p1)
        p1p3 = self._subtractVec(p3, p1)

        plane_normal_vec = triangle.normal_vec

        # Find the distance between the plane and the origin point
        # plane_normal_len = self._lengthVec(plane_normal_vec)

        d = self._dotProduct(plane_normal_vec, p1)

        # Calculate P - - - 

        # Check if direction_vec and plane are parallel
        normal_dot_dir = self._dotProduct(plane_normal_vec, direction_vec)

        if normal_dot_dir < EPSILON and normal_dot_dir > 0: # If the dot product is practically zero, they are parallel
            return math.inf
        
        # Compute d
        d = self._dotProduct(plane_normal_vec, p1)

        # Compute t
        t = (d - self._dotProduct(plane_normal_vec, origin)) / normal_dot_dir

        # Check if the triangle is behind the ray
        if t < 0: return math.inf

        # Compute the point of intersection
        p = self._addVec(origin, self._multiplyVec(t, direction_vec))

        # Inside-Out Test - - - 

        p1p = self._subtractVec(p, p1)

        p2p3 = self._subtractVec(p3, p2)
        p2p = self._subtractVec(p, p2)
        p3p1 = self._subtractVec(p1, p3)
        p3p = self._subtractVec(p, p3)

        u = self._crossProduct(p1p2, p1p)
        v = self._crossProduct(p2p3, p2p)
        w = self._crossProduct(p3p1, p3p)
        
        # Check if the point is inside the triangle using the barycentric coordinates
        if (self._dotProduct(u, v) >= 0) and (self._dotProduct(v, w) >= 0):
            return t
        else:
            return math.inf

    def _calculateClosestIntersection(self, origin, direction_vec, t_min, t_max):
        closest_obj = None
        closest_t = math.inf

        for world_obj in self.world.objects:

            if world_obj.__class__.__name__ == "Sphere":
                t_1, t_2 = self._intersectRaySphere(origin, direction_vec, world_obj)
                if t_min < t_1 < t_max and t_1 < closest_t:
                    closest_t = t_1
                    closest_obj = world_obj
                if t_min < t_2 < t_max and t_2 < closest_t:
                    closest_t = t_2
                    closest_obj = world_obj
            elif world_obj.__class__.__name__ == "Triangle":
                t_1 = self._intersectRayTriangle(origin, direction_vec, world_obj)
                if t_min < t_1 < t_max and t_1 < closest_t:
                    closest_t = t_1
                    closest_obj = world_obj

        return closest_obj, closest_t
    
    def _traceRay(self, origin, direction_vec, t_min, t_max, recursion_depth:int=3):
        closest_obj, closest_t = self._calculateClosestIntersection(origin, direction_vec, t_min, t_max)
        if closest_obj == None:
            return self.background_color
        
        # Compute intersection
        # point = origin + closest_t * direction_vec
        point = self._addVec(origin, self._multiplyVec(closest_t, direction_vec))

        # Compute sphere normal at intersection
        if closest_obj.__class__.__name__ == "Sphere":
            normal_vec = self._subtractVec(point, closest_obj.position)
        elif closest_obj.__class__.__name__ == "Triangle":
            normal_vec = closest_obj.normal_vec
            
        # Normalize
        normal_length = self._lengthVec(normal_vec)

        # prevent division by zero by adding EPSILON
        if normal_length == 0: normal_length += EPSILON
        
        normal_vec = self._multiplyVec(1.0 / normal_length, normal_vec)

        # View vector is simply the inverse of the ray direction vector
        view_vec = self._multiplyVec(-1, direction_vec)

        lighting = self._computeLighting(point, normal_vec, view_vec, closest_obj.specular)
        local_color = self._multiplyVec(lighting, closest_obj.color)

        if closest_obj.reflective <= 0 or recursion_depth <= 0:
            return self._clampColorVec(local_color)
        
        reflected_vec = self._reflectVec(view_vec, normal_vec)
        reflected_color = self._traceRay(point, reflected_vec, EPSILON, math.inf, recursion_depth-1)


        local_color = self._addVec(self._multiplyVec(1 - closest_obj.reflective, local_color), self._multiplyVec(closest_obj.reflective, reflected_color))
        return self._clampColorVec(local_color)

    def render(self) -> Image:
        """Renders the scene and returns a PIL Image.
        """

        # Create basis image and context
        self.image = Image.new("RGB", (self.width, self.height), self.background_color)
        self.ctx = ImageDraw.Draw(self.image)

        origin = (0, 0, 0) # defines origin of world space

        for x in range(-self.width // 2, self.width // 2):
            for y in range(-self.height // 2, self.height // 2):
                direction_vec = self._canvasToViewport(x, y)
                
                # Apply camera rotation matrix
                direction_vec = self._multiplyMat(self.camera_rotation, direction_vec)

                color = self._traceRay(self.camera_position, direction_vec, 1, math.inf, 3)
                
                if color:
                    self._putPixel(x, y, color)

        return self.image

    def setCameraRotation(self, rotation_mat:list[list]) -> None:
        self.camera_rotation = rotation_mat

    def setCameraPosition(self, position_vec:tuple[float]) -> None:
        self.camera_position = position_vec

    def _putPixel(self, x:int, y:int, color:tuple=(0, 0, 0)) -> None:
        """Places a pixel relative to the origin defined at the center of the canvas.
        Conforms to formulas given on page 3 of CGFS.
        Args:
            x (int): x-pos relative to canvas center
            y (int): y-pos relative to canvas center
            color (tuple, optional): (R3, G3, B3). Defaults to (0, 0, 0).
        """

        screen_x = (self.width / 2) + x
        screen_y = (self.height / 2) - y
        
        self.ctx.point((screen_x,screen_y), color)

    def saveFile(self, filename:str="untitled", format:str="png") -> None:
        """Saves the current canvas to a PNG file with the specified name.

        Args:
            filename (str): filename
        """
        self.image.save(f"{filename}.{format}")