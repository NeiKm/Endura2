from ursina import *
from core.ObjectFactory import ObjectFactory
from entities.player import Player
from ursina.shaders import lit_with_shadows_shader

class FlatWorld(Entity):
    def __init__(self, factory):
        super().__init__()
        floor_size = 64
        spacing = 1
        world = factory.create_entity(
            model='vr_modern_gallery_room (1).glb',
            scale=1.5,
            position=(0, 0, 0),
            double_sided=True,
            collider='box'
        )

class MainScene(Entity):
    def __init__(self):
        super().__init__()

        self.player = Player()
        self.factory = ObjectFactory()

        self.world = FlatWorld(self.factory)

        DirectionalLight(shadows=True, rotation=(45, -45, 45))

    def input(self, key):
        if key == "escape":
            application.quit()