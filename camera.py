from math import tan,pi

class Camera:
    def __init__(self, pos=(0,0,0), rot=(0,0,0), fov=80.0, znear=1.0, zfar=50.0) -> None:
        self.pos = pos; self.rot = rot;
        self.fov = fov; self.znear = znear; self.zfar = zfar;
        self.f = 1 / tan(fov * 0.5 / 180 * pi);