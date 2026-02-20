from ursina import *
from core.ObjectFactory import ObjectFactory
from entities.player import Player
from ursina.shaders import lit_with_shadows_shader
from core.utils import LoadMap
from ursina.physics import *

class Object(Entity, ObjectFactory, LoadMap): 
    def __init__(self): 
        super().__init__() 
        self.floor_size = 64 
        self.json_object() 
        self.table()
        self.sky = Sky(texture="static/textures/sky_texture2.jpg")

    def json_object(self): 
        self.world = self.load_map("scenes\main_scene\world.json")
        for i in self.world:
            i.texture = None

    def table(self):
        self.table_ = Entity(
            model="static/3d_model/table.glb",
            position=(0, -2, 4),
            scale=4,
            collider="box",
            texture=None,
            color=color.white
        )

    def table_glith_1(self):
        destroy(self.table_)
        self.table_ = Entity(
            model="static/3d_model/table.glb",
            position=(0, -2, 4),
            scale=4,
            collider="box",
            texture="static/textures/miniglith.png",
        )
        invoke(self.table_glith_2, delay=0.1)

    def table_glith_2(self):
        destroy(self.table_)
        self.table_ = Entity(
            model="static/3d_model/table.glb",
            position=(0, -2, 4),
            scale=4,
            collider="box",
            texture=None,
            color=color.white
        )
        invoke(self.table_glith_1, delay=random.randint(1, 2))

    def sky_glith_1(self):
        destroy(self.sky)
        self.sky = Sky(texture="static/textures/glith.jpg")
        invoke(self.sky_glith_2, delay=0.1)

    def sky_glith_2(self):
        destroy(self.sky)
        self.sky = Sky(texture="static/textures/sky_texture2.jpg")
        invoke(self.sky_glith_1, delay=random.randint(1, 6))
    
    def update(self):
        pass


class MainCutScene(Entity):
    def __init__(self, player):
        super().__init__()
        self.player = player
        invoke(self.wake_up_, delay=1)

    def wake_up_(self):
        self.player.wake_up(with_blink=False, duration=6)

    def close_eyes_(self):
        self.player.close_eyes()
        

class MainScene(Object):
    def __init__(self):
        super().__init__()

        self.player = Player()
        self.cut_scene = MainCutScene(self.player)
        # self.player.add_item("Веревка") ИСПРАВИТЬ (ДОБАВЛЕНИЕ ПРЕДМЕТОВ НЕ РАБОТАЕТ)

        self.setup_light()
        self.setup_sounds()

        invoke(self.table_glith_1, delay=1)
        invoke(self.sky_glith_1, delay=1)


    def setup_light(self):
        sun = DirectionalLight(
            shadows=True,
            shadow_resolution=(4096, 4096),
        )
        sun.look_at(Vec3(1, -1, -1))
        sun.shadow_map_resolution = Vec2(4096, 4096)
        sun.shadow_bias = 0.01

    def setup_sounds(self):
        self.bg_music = Audio(
            "static/sounds/music/first_scene_bg.mp3",
            loop=True,
            autoplay=True
        )

    def setup_room_light(parent=None):
        light = PointLight(
            parent=parent,
            position=(0, 2, 0),
            shadows=True
        )
        light.color = color.white
        light.radius = 10

    def input(self, key):
        if key == "escape":
            application.quit()

    def update(self):
        self.ray = raycast(
            origin=camera.world_position,
            direction=camera.forward,
            distance=2,
            ignore=(self.player,)
        )
        if self.ray.hit and self.ray.entity == self.world[12] or self.ray.entity == self.world[11]:
            self.world[12].color = color.green
            self.world[11].color = color.green
        else:
            self.world[12].color = color.white
            self.world[11].color = color.white
