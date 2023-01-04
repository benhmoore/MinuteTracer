from PIL import Image, ImageDraw
import math
from math import inf, sqrt

class Renderer:
    def __init__(self, world, pixel_dimensions:tuple, background_color:tuple=(255,255,255)):
        self.world = world
        self.width, self.height = pixel_dimensions
        self.background_color = background_color

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

    def _subtractVec(self, a:tuple, b:tuple) -> tuple[float]:
        return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
    
    def _multiplyVec(self, k:float, vec:tuple) -> tuple[float]:
        return (k*vec[0], k*vec[1], k*vec[2])

    def _addVec(self, a:tuple, b:tuple) -> tuple[float]:
        return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

    def _lengthVec(self, a:tuple) -> float:
        return sqrt(self._dotProduct(a, a))

    def _clampColorVec(self, color_vec) -> tuple[int]:
        """Clamps a color vector to integer values between 0 and 255.
        """
        return (
                int(min(255, max(0, color_vec[0]))),
                int(min(255, max(0, color_vec[1]))),
                int(min(255, max(0, color_vec[2]))),
            )

    def _computeLighting(self, point_vec, normal_vec, view_vec, specular):
        intensity = 0.0
        length_normal = self._lengthVec(normal_vec)
        length_V = self._lengthVec(view_vec)

        if len(self.world.getLights()) < 1:
            return 1.0

        for light in self.world.getLights():
            if light.__class__.__name__ == 'AmbientLight':
                intensity += light.intensity
            else: 
                if light.__class__.__name__ == 'PointLight':
                    L = self._subtractVec(light.position, point_vec)
                else:
                    L = light.direction

                # Diffuse
                normal_dot_L = self._dotProduct(normal_vec, L)
                if normal_dot_L > 0:
                    intensity += (light.intensity * normal_dot_L) / (length_normal * self._lengthVec(L))
        
                # Specular
                if specular != -1:
                    R_vec = self._subtractVec(self._multiplyVec(2.0 * self._dotProduct(normal_vec, L), normal_vec), L)
                    R_dot_V = self._dotProduct(R_vec, view_vec)
                    if R_dot_V > 0:
                        intensity += light.intensity * math.pow(R_dot_V / (self._lengthVec(R_vec) * length_V), specular)
        return intensity

    def _intersectRaySphere(self, camera_vec, direction_vec, world_obj):
        
        # Hardcoded to assume all objects are spheres
        CO = self._subtractVec(camera_vec, world_obj.position)

        a = self._dotProduct(direction_vec, direction_vec)
        b = 2*self._dotProduct(CO, direction_vec)
        c = self._dotProduct(CO, CO) - world_obj.radius**2

        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return inf, inf
        
        t_1 = (-b + sqrt(discriminant)) / (2*a)
        t_2 = (-b - sqrt(discriminant)) / (2*a)

        return t_1, t_2
    
    def _traceRay(self, camera_vec, direction_vec, t_min, t_max):
        closest_t = inf
        closest_sphere = None

        self.world.getLights()

        for world_obj in self.world.objects:

            t_1, t_2 = self._intersectRaySphere(camera_vec, direction_vec, world_obj)
            if (t_1 <= t_max and t_1 >= t_min) and t_1 < closest_t:
                closest_t = t_1
                closest_sphere = world_obj
            
            if (t_2 <= t_max and t_2 >= t_min) and t_2 < closest_t:
                closest_t = t_2
                closest_sphere = world_obj

        if closest_sphere == None:
            return None
        
        # Compute intersection
        # point_vec = camera_vec + closest_t * direction_vec
        point_vec = self._addVec(camera_vec, self._multiplyVec(closest_t, direction_vec))

        # Compute sphere normal at intersection
        normal_vec = self._subtractVec(point_vec, closest_sphere.position)

        # Normalize
        normal_vec = self._multiplyVec(1.0 / self._lengthVec(normal_vec), normal_vec)

        # View vector is simply the inverse of the ray direction vector
        view_vec = self._multiplyVec(-1, direction_vec)

        lighting = self._computeLighting(point_vec, normal_vec, view_vec, closest_sphere.specular)
        computed_color_vec = self._multiplyVec(lighting, closest_sphere.color)

        return self._clampColorVec(computed_color_vec)

    def render(self) -> Image:
        """Renders the scene and returns a PIL Image.
        """

        # Create basis image and context
        self.image = Image.new("RGB", (self.width, self.height), self.background_color)
        self.ctx = ImageDraw.Draw(self.image)

        camera_vec = (0, 0, 0) # defines origin of world space

        for x in range(-self.width // 2, self.width // 2):
            for y in range(-self.height // 2, self.height // 2):
                direction_vec = self._canvasToViewport(x, y)
                color = self._traceRay(camera_vec, direction_vec, 1, inf)
                
                if color:
                    self.putPixel(x, y, color)

        return self.image

    def putPixel(self, x:int, y:int, color:tuple=(0, 0, 0)) -> None:
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