from src.mesh.mesh import Mesh

class ObjParser:
    @staticmethod
    def Parse(file="") -> Mesh:

        vertices = []
        faces = []

        with open(file) as obj:
            lines = obj.readlines()
            for i in lines:
                if (i[0] != "v" and i[0] != "f") or i[1] != " ": continue
                
                if i[0] == "v":
                    vertices.append(i.rstrip()[2:].split(" "))
                elif i[0] == "f":
                    face = []
                    for a in i.rstrip()[2:].split(" "):
                        if len(face) == 3: break
                        face.append(a.split("/")[0])
                        
                    faces.append(face)

        return Mesh(verts=vertices , faces=faces)