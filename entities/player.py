from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import math

class Player(FirstPersonController):

    def __init__(self):
        super().__init__()
        self.player_model = Entity(
            parent=self,
            y=1,
            z=-0.2,
            scale=2,
            rotation_y=-90,
            model="static/3d_model/Player.glb",
            shader = lit_with_shadows_shader,
            cast_shadows=True,
            receive_shadows=True
        )

        # Праметры
        self.position = (0, -1, 0)
        self.cursor.visible = True
        self.cursor.scale = 0.004
        self.cursor.model = "circle"
        self.cursor.color = color.green
        self.speed = 5
        self.gravity = 0.5
        self.jump_height = 2
        self.camera_pivot.y = 1.85
        self.fly_mode = [self.gravity, False]

        # -------------------реализация состаяние граз-------------------
        self.eye_condition = False
        self.eye_busy = False
        self.eye_height = 1.01
        self.eye_state = "open" # для переключения одной кнопкой

        self.top_eye = Entity(
            parent = camera.ui,
            model = "quad",
            color = color.black,
            scale = (2, self.eye_height),
            position = (0,  0.5),
            z=-1
        )

        self.bottom_eye = Entity(
            parent = camera.ui,
            model = "quad",
            color = color.black,
            scale = (2, self.eye_height),
            position = (0, -0.5),
            z=-1
        )
        invoke(self.wake_up, delay=0.1)
        # -------------------реализация состаяние диалога-------------------
        self.dialog_fill_text = "asdadasdasdasda"
        self.dialog_text = ""
        self.dialog = False
        self.text_index = 0
        self.text_speed = 0.2
        self.dialog_ui = Text(
            text="",
            parent=camera.ui,
            scale=3,
            color=color.black,
            origin=(0, 0),
            position=(0, -0.3),
            enabled=False   # <- Скрытие субтитров
        )

        self.shake_timer = 0
        self.shake_power = 0.06
        self.shake_speed = 12


    def update(self):
        super().update()

        if self.dialog:
            self.dialog_ui.enabled = True

            if self.text_index < len(self.dialog_fill_text):
                self.text_index += self.text_speed
                self.dialog_ui.text = self.dialog_fill_text[:int(self.text_index)]
        else:
            self.dialog_ui.enabled = False

        if held_keys["e"]:
            self.position += Vec3(0, 0.5, 0)  
        if held_keys["q"]:
            self.position -= Vec3(0, 0.5, 0)  

        if not self.fly_mode:
            if held_keys["shift"]:
                self.speed = 10
            else:
                self.speed = 5
            self.camera_shaking()
    

    def input(self, key):
        super().input(key)

        if key == "alt":
            mouse.locked = not mouse.locked
            self.cursor.visible = not self.cursor.visible
        if key == 'c':
            self.eye_state = "close" if self.eye_state == "open" else "open" 
            self.eyes(movement = self.eye_state)

        if key == "r":
            self.dialog = not self.dialog
            if self.dialog:
                self.text_index = 0
                self.dialog_ui.text = ""

        if key == "f":
            self.fly_mode[1] = not self.fly_mode[1]
            if self.fly_mode[1]:
                self.gravity = 0
                self.speed = 20
            elif not self.fly_mode[1]:
                self.speed = 5
                self.gravity = self.fly_mode[0]


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


    def wake_up(self):

        if self.eye_busy:
            return
        camera.fov = 120
        camera.animate("fov", 90, duration = 2, curve = curve.out_quad)
        # camera.shake(duration=1, magnitude=0.5)
        self.eye_busy = True
        self.eye_condition = False

        invoke(self._wake_phase_one, delay=0.4)


    def _wake_phase_one(self):
        h = self.eye_height * 0.4

        self.top_eye.animate(
            "scale_y", h,
            duration=0.5,
            curve=curve.out_expo
        )
        self.bottom_eye.animate(
            "scale_y", h,
            duration=0.5,
            curve=curve.out_expo
        )

        invoke(self._wake_phase_two, delay=0.55)


    def _wake_phase_two(self):
        self.top_eye.animate(
            "scale_y", self.eye_height * 0.25,
            duration=0.12,
            curve=curve.in_out_sine
        )
        self.bottom_eye.animate(
            "scale_y", self.eye_height * 0.25,
            duration=0.12,
            curve=curve.in_out_sine
        )

        invoke(self._wake_phase_three, delay=0.15)


    def _wake_phase_three(self):

        self.top_eye.animate(
            "scale_y", 0,
            duration=0.35,
            curve=curve.out_cubic
        )
        self.bottom_eye.animate(
            "scale_y", 0,
            duration=0.35,
            curve=curve.out_cubic
        )

        self.eye_condition = True
        invoke(
            setattr, self, 
            "eye_busy", False, 
            delay=0.1
        )
        invoke(
            self.eyes,
            movement = "close",
            duration = 0.25,
            delay = 0.11
        )
        invoke(
            self.eyes,
            movement = "open",
            duration = 0.25,
            delay = 0.20
        )


    def dialogue_subtitles(self, full_text):
        self.dialog_fill_text = full_text
        self.text_index = 0
        self.dialog_ui.text = ""
        self.dialog = True



    def UI(self):
        if self.dialog:
            pass


    def eyes(
            self,
            movement = "open",
            blur = False,
            blur_power = 0.1,
            effect_type = None,
            duration = 0.5
    ):
        if self.eye_busy:
            return
        

        if movement == "close" and self.eye_condition:
            self.top_eye.scale_y = 0
            self.bottom_eye.scale_y = 0

            self.top_eye.animate(
                "scale_y", 
                self.eye_height,
                curve = curve.out_expo,
                duration=duration
            )
            self.bottom_eye.animate(
                "scale_y", 
                self.eye_height,
                curve = curve.out_expo,
                duration=duration
            )

            self.eye_condition = False
            invoke(
                setattr, self, 
                "eye_busy", False, 
                delay = duration
            )
        elif movement == "open" and not self.eye_condition:
            self.top_eye.animate(
                "scale_y", 
                0,
                curve = curve.out_expo,
                duration = duration,
            )
            self.bottom_eye.animate(
                "scale_y", 
                0,
                curve = curve.out_expo,
                duration = duration
            )

            self.eye_condition = True

            invoke(
                setattr, self, 
                "eye_busy", False, 
                delay = duration
            )
        return
