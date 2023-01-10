from PIL import Image, ImageDraw
from lib import math_functions

import math, time

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

    def _computeLighting(self, point, normal_vec, view_vec, specular):
        intensity = 0.0
        length_normal = math_functions._lengthVec(normal_vec)
        length_view = math_functions._lengthVec(view_vec)

        if len(self.world.getLights()) < 1:
            return 1.0

        for light in self.world.getLights():
            if light.__class__.__name__ == 'AmbientLight':
                intensity += light.intensity
            else:
                if light.__class__.__name__ == 'PointLight':
                    L = math_functions._subtractVec(light.position, point)
                    t_max = 1.0 - EPSILON
                else:
                    L = light.direction
                    t_max = math.inf

                # Shadow check
                shadow, _ = self._calculateClosestIntersection(point, L, EPSILON, t_max)
                if shadow: continue

                if math_functions._dotProduct(normal_vec, L) < 0 and math_functions._dotProduct(normal_vec, view_vec) < 0:
                    normal_vec = math_functions._multiplyVec(-1, normal_vec)
                elif math_functions._dotProduct(normal_vec, L) > 0 and math_functions._dotProduct(normal_vec, view_vec) < 0:
                    normal_vec = math_functions._multiplyVec(-1, normal_vec)

                # Diffuse
                normal_dot_L = math_functions._dotProduct(normal_vec, L)

                if normal_dot_L > 0:
                    intensity += (light.intensity * normal_dot_L) / (length_normal * math_functions._lengthVec(L))
        
                    # Specular
                    if specular != -1:
                        R_vec = math_functions._reflectVec(L, normal_vec)
                        R_dot_V = math_functions._dotProduct(R_vec, view_vec)
                        if R_dot_V > 0:
                            intensity += light.intensity * math.pow(R_dot_V / (math_functions._lengthVec(R_vec) * length_view), specular)
        return intensity

    def _intersectRaySphere(self, origin, direction_vec, sphere):
        CO = math_functions._subtractVec(origin, sphere.position)

        a = math_functions._dotProduct(direction_vec, direction_vec)
        b = 2 * math_functions._dotProduct(CO, direction_vec)
        c = math_functions._dotProduct(CO, CO) - sphere.radius_sq

        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return math.inf, math.inf
        
        t_1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t_2 = (-b - math.sqrt(discriminant)) / (2 * a)

        return t_1, t_2

    def _intersectRayTriangle(self, origin, direction_vec, triangle):
        p1, p2, p3 = triangle.points

        # Calculate P - - - 

        # Check if direction_vec and plane are parallel
        normal_dot_dir = math_functions._dotProduct(triangle.normal_vec, direction_vec)

        if math.isclose(normal_dot_dir, 0, rel_tol=EPSILON): # If the dot product is practically zero, they are parallel
            return math.inf
        
        # Compute t
        if triangle.normal_dot_origin == None or triangle.ray_origin != origin:
            triangle.normal_dot_origin = math_functions._dotProduct(triangle.normal_vec, origin)
            triangle.ray_origin = origin

        t = (triangle.d - triangle.normal_dot_origin) / (normal_dot_dir + EPSILON)

        # Check if the triangle is behind the ray
        if t < 0: return math.inf

        # Compute the point of intersection
        p = math_functions._addVec(origin, math_functions._multiplyVec(t, direction_vec))

        # Inside-Out Test - - - 
        p1p = math_functions._subtractVec(p, p1)
        p2p = math_functions._subtractVec(p, p2)
        p3p = math_functions._subtractVec(p, p3)

        u = math_functions._crossProduct(triangle.p1p2, p1p)
        v = math_functions._crossProduct(triangle.p2p3, p2p)
        w = math_functions._crossProduct(triangle.p3p1, p3p)
        
        # Check if the point is inside the triangle using the barycentric coordinates
        if (math_functions._dotProduct(u, v) >= 0) and (math_functions._dotProduct(v, w) >= 0):
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
        point = math_functions._addVec(origin, math_functions._multiplyVec(closest_t, direction_vec))

        # Compute sphere normal at intersection
        if closest_obj.__class__.__name__ == "Sphere":
            normal_vec = math_functions._subtractVec(point, closest_obj.position)
        elif closest_obj.__class__.__name__ == "Triangle":
            normal_vec = closest_obj.normal_vec
            
        # Normalize
        normal_length = math_functions._lengthVec(normal_vec)

        # prevent division by zero by adding EPSILON
        if normal_length == 0: normal_length += EPSILON
        
        normal_vec = math_functions._multiplyVec(1.0 / normal_length, normal_vec)

        # View vector is simply the inverse of the ray direction vector
        view_vec = math_functions._multiplyVec(-1, direction_vec)

        lighting = self._computeLighting(point, normal_vec, view_vec, closest_obj.specular)
        local_color = math_functions._multiplyVec(lighting, closest_obj.color)

        if closest_obj.reflective <= 0 or recursion_depth <= 0:
            return math_functions._clampColorVec(local_color)
        
        reflected_vec = math_functions._reflectVec(view_vec, normal_vec)
        reflected_color = self._traceRay(point, reflected_vec, EPSILON, math.inf, recursion_depth-1)


        local_color = math_functions._addVec(math_functions._multiplyVec(1 - closest_obj.reflective, local_color), math_functions._multiplyVec(closest_obj.reflective, reflected_color))
        return math_functions._clampColorVec(local_color)

    def render(self) -> Image:
        """Renders the scene and returns a PIL Image.
        """

        start_time = time.perf_counter()

        # Create basis image and context
        self.image = Image.new("RGB", (self.width, self.height), self.background_color)
        self.ctx = ImageDraw.Draw(self.image)

        for x in range(-self.width // 2, self.width // 2):
            for y in range(-self.height // 2, self.height // 2):
                direction_vec = self._canvasToViewport(x, y)
                
                # Apply camera rotation matrix
                direction_vec = math_functions._multiplyMat(self.camera_rotation, direction_vec)

                color = self._traceRay(self.camera_position, direction_vec, 1, math.inf, 3)
                
                if color:
                    self._putPixel(x, y, color)

        
        end_time = time.perf_counter()

        print(f"Frame render time: {round(end_time - start_time, 2)} sec")

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