from ursina import *
from entity import EntityManager

class Rendering:

    def __init__(self):
        self.ground = self.flor()

    def flor(self):
        self.ground = Entity(
            model = "cube",
            texture = Texture("static/textures/grid.PNG"),
            texture_scale = (50, 50),
            scale = (100, 0.5, 100),
            collider = "box",
            position = Vec3(0, -4, 0)
        )
        return self.ground
    