from math import tan,pi

class Camera:
    def __init__(self, pos=(0,0,0), rot=(0,0,0), fov=80.0, znear=1.0, zfar=50.0) -> None:
        self.pos = pos; self.prev_pos = 0; 
        self.rot = rot; self.prev_rot = 0;

        self.fov = fov; self.znear = znear; self.zfar = zfar;
        self.f = 1 / tan(fov * 0.5 / 180 * pi);

    def Update(self) -> None:
        if (self.prev_pos != self.pos): 
            self.prev_pos = self.pos.copy();
        
        if (self.prev_rot != self.rot):
            self.prev_rot = self.rot.copy()