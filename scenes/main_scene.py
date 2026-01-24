from ursina import *
from core.ObjectFactory import ObjectFactory
from entities.player import Player
from ursina.shaders import lit_with_shadows_shader

class FlatWorld(Entity):
    def __init__(self, factory):
        super().__init__()
        floor_size = 64
        spacing = 1
        self.test_platform = factory.create_entity(
            model="cube",
            texture = "grass",
            scale = (floor_size, 1, floor_size),
            position = (0, -2, 0),
            parent = self
        )
        self.test_cube = factory.create_entity(
            model = "cube",
            texture = "white_cube",
            scale = (1, 1, 1),
            position =  (0, 0, 7),
            color = color.gray,
            parent = self
        )
        # world = factory.create_entity(
        #     model='vr_modern_gallery_room (1).glb',
        #     scale=1.5,
        #     position=(0, 0, 0),
        #     double_sided=True,
        #     collider='box'
        # )
        

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

    def update(self):
        self.world.test_cube.rotation += Vec3(30, 60, 0) * time.dt
