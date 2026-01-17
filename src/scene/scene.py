import uuid

class Scene:
    def __init__(self , objects=[]) -> None:
        self.objects = objects
        self.uuid = str(uuid.uuid4()) 