from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

class Player(FirstPersonController):
    def __init__(self):
        super().__init__()

        # Праметры
        self.cursor.visible = True
        self.cursor.scale = 0.004
        self.cursor.model = "circle"
        self.cursor.color = color.green
        self.speed = 5
        self.gravity = 0.5
        self.jump_height = 2
        self.camera_pivot.y = 1.8
        self.height = 2
        self.position = (0, 0)

        # self.dialog = False
        # self.ui = self.UI()
        self.default_shader = lit_with_shadows_shader

    def update(self):
        super().update()
        if held_keys["shift"]:
            self.speed = 8
        else:
            self.speed = 5
    
    def input(self, key):
        super().input(key)

        if key == "alt":
            mouse.locked = not mouse.locked
            self.cursor.visible = not self.cursor.visible

    def UI(self):
        self.dialog_box = Entity(
            parent=camera.ui,
            model="cube",
            color=color.gray,
            scale=(1, 0.2, 1),
            position=(0, -0.4)
        )
