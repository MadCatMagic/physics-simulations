import math

# --- Vector Classes ---
class v2:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return v2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return v2(self.x - other.x, self.y - other.y)
    
    def __truediv__(self, scalar):
        return v2(self.x / scalar, self.y / scalar)

    def __mul__(self, scalar):
        return v2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def normalise(self):
        l = self.length()
        return v2(self.x / l, self.y / l) if l != 0 else v2()

    #def to_int_tuple(self):
    #    return (int(self.x), int(self.y))

    def __repr__(self):
        return f"v2({self.x}, {self.y})"

class v3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return v3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar):
        return v3(self.x * scalar, self.y * scalar, self.z * scalar)

    #def to_color_tuple(self):
    #    return (int(self.x), int(self.y), int(self.z))

    def __repr__(self):
        return f"v3({self.x}, {self.y}, {self.z})"