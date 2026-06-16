from ursina import *
from core.ObjectFactory import ObjectFactory
from entities.player import Player
from ursina.shaders import lit_with_shadows_shader
from core.utils import LoadMap
from ursina.physics import *
from entities.enemy import Monster
import math
import random

class Object(Entity, ObjectFactory, LoadMap): 
    def __init__(self): 
        super().__init__() 
        # self.table()``
        self.sky = Sky(texture="static/textures/sky.png")
        # ----это что-бы не вылетало---
        # self.room2 = []
        # self.room3 = []
        # self.room4 = []
        # self.room5 = []
        # self.room6 = []
        # self.room7 = []
        self.floor_size = 64
        self.current_z = 0



        self.last_room = None
        self.room_files = [
            "scenes/room2/room2.json",
        ]

        # self.room1_()
        self.map()

    """Временные меры для геймджема!!!"""
    def map(self):
        Entity(
            model = "backroom_this_model_will_give_you_nightmare.glb",
            shader = lit_with_shadows_shader,
            position = Vec3(3, 0, 0),
            collider="mesh",
            scale = 2
        )

    def ramdom_generate_room(self):
        rooms = []
        pass

    def room1_(self):
        self.last_room = self.load_map(
            "scenes/main_scene/world.json",
            displacement=Vec3(0, 0, self.current_z)
        )

        length = self.get_room_length(self.last_room)
        self.current_z -= (length + 2)

    def room3_(self):
        pass

    def get_room_length(self, room_entities):
        min_z = float("inf")
        max_z = float("-inf")
    
        for e in room_entities:
            z = e.world_position.z
            size = e.scale_z
    
            min_z = min(min_z, z - size/2)
            max_z = max(max_z, z + size/2)
    
        return max_z - min_z

    def table(self):
        self.table_ = Entity(
            model="static/3d_model/table.glb",
            position=(0, -2, 4),
            scale=4,
            collider="box",
            texture=None,
            color=color.white
        )

    # Это временные меры, этот код отвечал за глитч текстур на столе.
    # Нужно переписать данный код и желательно сделать отдельный метод для гтичей Entity
    # def table_glith_1(self):
    #     destroy(self.table_)
    #     self.table_ = Entity(
    #         model="static/3d_model/table.glb",
    #         position=(0, -2, 4),
    #         scale=4,
    #         collider="box",
    #         texture="static/textures/miniglith.png",
    #     )
    #     invoke(self.table_glith_2, delay=0.1)

    # def table_glith_2(self):
    #     destroy(self.table_)
    #     self.table_ = Entity(
    #         model="static/3d_model/table.glb",
    #         position=(0, -2, 4),
    #         scale=4,
    #         collider="box",
    #         texture=None,
    #         color=color.white
    #     )
    #     invoke(self.table_glith_1, delay=random.randint(1, 2))

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
        self.player.position += Vec3(0, 4, 0)
        self.monster = Monster(self.player)
        self.setup_light()
        self.setup_sounds()
        self.cut_scene = MainCutScene(self.player)
        self.pickups = []
        self.spawn_pickups()

        # invoke(self.table_glith_1, delay=1)
        # invoke(self.sky_glith_1, delay=1)

        self.rk_boss = Entity(
            model = "static/3d_model/rocket_boss.glb",
            shader = lit_with_shadows_shader,
            parent = camera.ui,
            position = (-0.7, -0.4),
            rotation = Vec3(0, 90, 0),
            scale = 0.3
        )
        self.player.dialog = True
        self.player.text_speed = 1


        """
            Код грязный, но это временно
            Желательно заменить все что ниже на функцию или класс который будет отвечать за отрисовку субтитров
        """ 
        invoke(self.player.dialogue_subtitles, "Привет…", delay=3)

        invoke(self.player.dialogue_subtitles,
               "Не пугайся. Хотя… наверное уже поздно.",
               delay=6)

        invoke(self.player.dialogue_subtitles,
               "Да, это я. Фигурка, которую ты купил на ярмарке.",
               delay=10)

        invoke(self.player.dialogue_subtitles,
               "Помнишь продавца? Он слишком улыбался.",
               delay=14)

        invoke(self.player.dialogue_subtitles,
               "Он забыл сказать одну маленькую деталь.",
               delay=18)

        invoke(self.player.dialogue_subtitles,
               "На мне было проклятие.",
               delay=22)

        invoke(self.player.dialogue_subtitles,
               "И теперь ты попал в нестабильный, багнутый слой реальности.",
               delay=26)

        invoke(self.player.dialogue_subtitles,
               "Это закулисье. Мир ошибок. Мир сбоев.",
               delay=30)

        invoke(self.player.dialogue_subtitles,
               "Здесь сама структура пространства иногда ломается.",
               delay=34)

        invoke(self.player.dialogue_subtitles,
               "Полы могут внезапно начать притягивать тебя вниз.",
               delay=38)

        invoke(self.player.dialogue_subtitles,
               "Если почувствуешь, что тебя тянет — просто прыгни.",
               delay=42)

        invoke(self.player.dialogue_subtitles,
               "Прыжок сбрасывает притяжение. Это сбой гравитации.",
               delay=46)

        invoke(self.player.dialogue_subtitles,
               "Но я не оставил тебя без защиты.",
               delay=50)

        invoke(self.player.dialogue_subtitles,
               "Я дал тебе техноочки.",
               delay=54)

        invoke(self.player.dialogue_subtitles,
               "В этом мире они способны закрывать твои глаза.",
               delay=58)

        invoke(self.player.dialogue_subtitles,
               "Когда ты закрываешь глаза — система перестаёт тебя отслеживать.",
               delay=62)

        invoke(self.player.dialogue_subtitles,
               "И монстр не может бежать за тобой.",
               delay=66)

        invoke(self.player.dialogue_subtitles,
               "Но помни — ты тоже ничего не видишь.",
               delay=70)

        invoke(self.player.dialogue_subtitles,
               "Потому что здесь есть существо.",
               delay=74)

        invoke(self.player.dialogue_subtitles,
               "Красный монстр без облика.",
               delay=78)

        invoke(self.player.dialogue_subtitles,
               "Он выглядит как сфера чистой злобы.",
               delay=82)

        invoke(self.player.dialogue_subtitles,
               "Он — ошибка, которая научилась двигаться.",
               delay=86)

        invoke(self.player.dialogue_subtitles,
               "Если увидишь красное свечение — не стой. Беги.",
               delay=90)

        invoke(self.player.dialogue_subtitles,
               "Чтобы выбраться, тебе нужно собрать ключи.",
               delay=94)

        invoke(self.player.dialogue_subtitles,
               "Они разбросаны по этому сломанному миру.",
               delay=98)

        invoke(self.player.dialogue_subtitles,
               "Каждый ключ стабилизирует часть разлома.",
               delay=102)

        invoke(self.player.dialogue_subtitles,
               "Соберёшь все — откроется путь назад.",
               delay=106)

        invoke(self.player.dialogue_subtitles,
               "И, возможно… мы оба выберемся.",
               delay=110)

        invoke(self.player.dialogue_subtitles,
               "Но поторопись.",
               delay=114)

        invoke(self.player.dialogue_subtitles,
               "Он уже знает, что ты здесь.",
               delay=118)
        
        invoke(self.player.dialogue_subtitles,
               "[Shift]-спринт [c]-вкл/выкл технологию от рокетбосса [Tab]-инвентарь",
               delay=125)


    def spawn_next_room(self):

        room_path = random.choice(self.room_files)

        new_room = self.load_map(
            room_path,
            displacement=Vec3(0, 0, self.current_z)
        )

        length = self.get_room_length(new_room)
        self.current_z -= (length + 2)

        self.last_room = new_room


    def spawn_pickups(self):
        for i in range(18):
            block = Entity(
                model="static/3d_model/key.obj",
                color=color.yellow,
                scale=0.5,
                position=(
                    random.uniform(-20, 20),
                    1,
                    random.uniform(-40, 10)
                ),
                collider="box"
            )
            self.pickups.append(block)

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
        print(self.player.inventory)
        # if key == "escape":
        #     application.quit()
        # if key == "v":
        #     ray = self.player.shoot_ray(999)
        #     if "Key" in self.player.inventory:
        #         if ray.entity in self.last_room:
        #             ray.entity.animate(
        #                 "x",
        #                 10,
        #                 duration=1,
        #                 curve=curve.out_quad
        #             )

        #             self.spawn_next_room()
        #             self.player.remove_item("Key")



    def update(self):
        angle = (math.sin(time.time() * 1.5) * 10) + 90
        self.rk_boss.rotation_y = angle

        for block in self.pickups:
            if block and distance(self.player.position, block.position) < 1.5:
                destroy(block)
                self.pickups.remove(block)
                self.player.add_item("Key")