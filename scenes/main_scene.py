from ursina import *
from core.ObjectFactory import ObjectFactory
from entities.player import Player
from ursina.shaders import lit_with_shadows_shader
from core.utils import LoadMap

class FlatWorld(Entity, ObjectFactory):
    def __init__(self):
        super().__init__()
        
        self.room_floor = self.create_entity(
            model = "cube",
            texture = "white_cube",
            scale = (10, 1, 10),
            position =  (0, 0, 0),
            color = color.gray,
            parent = self
        )
        self.room_wall1 = self.create_entity(
            model = "cube",
            texture = "white_cube",
            scale = (1, 6, 10),
            position =  (5.3, 3, 0),
            color = color.gray,
            parent = self
        )
        self.room_wall2 = self.create_entity(
            model = "cube",
            texture = "white_cube",
            scale = (10, 6, 1),
            position =  (0, 3, 5.3),
            color = color.gray,
            parent = self
        )
        self.room_wall3 = self.create_entity(
            model = "cube",
            texture = "white_cube",
            scale = (1, 6, 10),
            position =  (-5.3, 3, 0),
            color = color.gray,
            parent = self
        )
        self.room_wall4 = self.create_entity(
            model = "cube",
            texture = "white_cube",
            scale = (10, 6, 1),
            position =  (0, 3, -5.3),
            color = color.gray,
            parent = self
        )
        self.room_ceiling = self.create_entity(
            model = "cube",
            texture = "white_cube",
            scale = (10, 1, 10),
            position =  (0, 5.5, 0),
            color = color.gray,
            parent = self
        )
        self.room_poster = self.create_entity(
            model = "quad",
            texture = "white_cube",
            scale = (1, 1.8, 1),
            position =  (0, 2, 4.),
            color = color.white,
            parent = self
        )
        
        

class MainScene(Entity, LoadMap):
    def __init__(self):
        super().__init__()

        self.player = Player()
        self.factory = ObjectFactory()

        self.world = FlatWorld()
        # self.load_map("world.json")
        DirectionalLight(shadows=True, rotation=(45, -45, 45))

    def input(self, key):
        if key == "escape":
            application.quit()
