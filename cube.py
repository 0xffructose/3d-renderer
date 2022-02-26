class Cube:
    def __init__(self,pos=(0,0,0),color="") -> None:
        self.verts = (-1+int(pos[0]),1+int(pos[1]),1+int(pos[2])),(1+int(pos[0]),1+int(pos[1]),1+int(pos[2])),(-1+int(pos[0]),-1+int(pos[1]),1+int(pos[2])),(1+int(pos[0]),-1+int(pos[1]),1+int(pos[2])),(-1+int(pos[0]),-1+int(pos[1]),-1+int(pos[2])),(1+int(pos[0]),-1+int(pos[1]),-1+int(pos[2])),(-1+int(pos[0]),1+int(pos[1]),-1+int(pos[2])),(1+int(pos[0]),1+int(pos[1]),-1+int(pos[2]))
        self.color = color