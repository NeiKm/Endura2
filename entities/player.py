from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import math

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

        self.shake_timer = 0
        self.shake_power = 0.06
        self.shake_speed = 12

        # self.dialog = False
        # self.ui = self.UI()
        self.default_shader = lit_with_shadows_shader

    def camera_shaking(self):
        is_moving = self.direction.length() > 0 and self.grounded

        if is_moving:
            current_shake_speed = self.shake_speed * 1.5 if held_keys['shift'] else self.shake_speed
            self.shake_timer += time.dt * current_shake_speed

            camera.x = math.cos(self.shake_timer * 0.5) * self.shake_power * 0.5
            camera.y = math.sin(self.shake_timer) * self.shake_power
        else:
            self.shake_timer = 0
            camera.x = lerp(camera.x, 0, time.dt * 10)
            camera.y = lerp(camera.y, 0, time.dt * 10)

    def update(self):
        super().update()
        if held_keys["shift"]:
            self.speed = 8
        else:
            self.speed = 5

        self.camera_shaking()
    
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
                