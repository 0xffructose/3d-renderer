import uuid

class Scene:
    def __init__(self) -> None:
        self.objects = []
        self.uuid = str(uuid.uuid4()) 