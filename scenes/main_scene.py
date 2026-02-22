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
        self.room1_()
        # self.table()
        self.sky = Sky(texture="static/textures/glith.jpg")

    def ramdom_generate_room(self):
        rooms = []
        pass

    def room1_(self): 
        self.room1 = self.load_map("scenes/main_scene/world.json")
    
    def room2_(self):
        self.room2 = self.load_map("scenes/room2/room2.json", displacement=Vec3(0, 0, 21))

    def room3_(self):
        pass

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

        # invoke(self.table_glith_1, delay=1)
        # invoke(self.sky_glith_1, delay=1)


    def setup_light(self):
        sun = DirectionalLight(
            shadows=True,
            shadow_resolution=(4096, 4096),
        )
        sun.look_at(Vec3(1, -1, -1))
        sun.shadow_map_resolution = Vec2(4096, 4096)
        sun.shadow_bias = 0.01

    def setup_sounds(self):
        # self.bg_music = Audio(
        #     "static/sounds/music/first_scene_bg.mp3",
        #     loop=True,
        #     autoplay=True
        # )
        pass

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
        if key == "v":
            ray = self.player.shoot_ray(99999)
            if ray.entity == self.room1[10]:
                print("____________________________________________")
                self.room1[10].animate(
                    "x",
                    10,
                    duration=1,
                    curve=curve.out_quad
                )
            if ray.entity == self.room1[-3]:
                print("____________________________________________")
                self.room1[-3].animate(
                    "x",
                    10,
                    duration=1,
                    curve=curve.out_quad
                )
                self.room2_()

            if ray.entity == self.room2[-3]:
                print("____________________________________________")
                self.room2[-3].animate(
                    "x",
                    10,
                    duration=1,
                    curve=curve.out_quad
                )



    def update(self):
        pass