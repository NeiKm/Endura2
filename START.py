from ursina import *
from ursina.shaders import lit_with_shadows_shader
from main import Main
import subprocess
import sys
import random
import os
import math


class EnduraMenu(Entity):
    def __init__(self):

        self.app = Ursina(title="Endura2 Menu (BETA)", borderless=False, fullscreen=False, resizable=True)
        super().__init__()
        window.color = color.rgb(15, 15, 25)
        window.fps_counter.enabled = False
        Sky(texture="static/textures/sky.png")

        AmbientLight(color=color.rgba(100, 100, 100, 100))
        DirectionalLight(color=color.white, direction=(0, 1, 10))

        self.model_pivot = Entity()
        camera.parent = self.model_pivot
        camera.position = (0, 0, -15)
        camera.look_at(self.model_pivot)

        self.models = [
            "static/3d_model/key.obj",
            "static/3d_model/Secret_key.obj",
            "static/3d_model/Player.glb",
            "static/3d_model/rocket_boss.glb",
            "static/3d_model/rocket_boss.glb"
        ]

        self.model_parameters = {
            "rotation":Vec3(0, 0, 0),
            "scale":3,
            "path":random.choice(self.models)
        }

        if self.model_parameters["path"] == "static/3d_model/Player.glb" or self.model_parameters["path"] == "static/3d_model/rocket_boss.glb":
            self.model_parameters["rotation"] = Vec3(0, 90, 0)
            self.model_parameters["scale"] = 6

        if os.path.exists(self.model_parameters["path"]):
            model_path = self.model_parameters["path"]
            # print(f"Loaded model: {self.model_parameters["path"]}")
        else:
            # print(f"Warning: Model {self.model_parameters["path"]} not found. Using placeholder.")
            model_path = "cube"

        self.hero_model = Entity(
            parent=self.model_pivot,
            model=model_path,
            color=color.yellow,
            scale=self.model_parameters["scale"],
            rotation=self.model_parameters["rotation"],
            shader=lit_with_shadows_shader
        )

        self.bg_music = Audio(
            "static/sounds/music/bfacb78306248c8.mp3",
            loop=True,
            autoplay=True
        )

        self.menu_ui = Entity(parent=camera.ui)
        menu_ui = self.menu_ui

        self.decor_line_left = Entity(
            parent=menu_ui,
            model="sphere",
            color=color.black,
            scale=(0.01, 0.5),
            position=(-0.5, 0),
            z=10
        )

        self.decor_line_right = Entity(
            parent=menu_ui,
            model="sphere",
            color=color.black,
            scale=(0.01, 0.5),
            position=(0.5, 0),
            z=10
        )

        class MenuButton(Button):
            def __init__(self, text, on_click, y_pos):
                super().__init__(
                    parent=menu_ui,
                    text=text,
                    text_color=color.white,
                    color=color.rgba(0, 0, 0, 180),
                    highlight_color=color.rgba(0, 150, 255, 220),
                    scale=(0.35, 0.07),
                    position=(0, y_pos),
                    origin=(0, 0),
                    text_size=1.3,
                    radius=0.15,
                )
                self.text_ = text
                self.on_click_func = on_click
                self.default_scale = (0.35, 0.07)
                self.hover_scale = (0.40, 0.08)
                
                self.glow = Entity(
                    parent=self,
                    model="quad",
                    color=color.rgba(0, 150, 255, 0),
                    scale=(1.2, 1.2),
                    z=-1
                )

            def on_mouse_enter(self):
                # self.animate_scale(self.hover_scale, duration=0.15)
                self.animate_color(color.rgba(0, 150, 255, 220), duration=0.15)
                self.text = self.text_
                # self.glow.animate_color(color.rgba(0, 150, 255, 100), duration=0.15)

            def on_mouse_exit(self):
                self.animate_scale(self.default_scale, duration=0.15)
                self.animate_color(color.rgba(0, 0, 0, 180), duration=0.15)
                self.glow.animate_color(color.rgba(0, 150, 255, 0), duration=0.15)
                self.text = self.text_
            
            def update(self):
                self.text = self.text_

            def on_click(self):
                self.animate_scale((0.32, 0.06), duration=0.05)
                if self.on_click_func:
                    self.on_click_func()

        def start_game():
            try:
                subprocess.Popen([sys.executable, "main.py"])
            except Exception as e:
                print(f"Error starting game: {e}")
            finally:
                exit()

        def quit_game():
            exit()

        self.title_main = Text(
            text="ENDURA 2",
            parent=menu_ui,
            y=0.25,
            origin=(0, 0),
            scale=4,
            color=color.rgb(0, 200, 255)
        )

        self.title_shadow = Text(
            text="ENDURA 2",
            parent=menu_ui,
            y=0.25,
            origin=(0, 0),
            scale=4.2,
            color=color.gray,
            z=1
        )

        # title_glow = Text(
        #     text="ENDURA 2",
        #     parent=menu_ui,
        #     y=0.25,
        #     origin=(0, 0),
        #     scale=4.5,
        #     color=color.rgba(0, 150, 255, 40),
        #     z=2
        # )

        self.subtitle = Text(
            text="Pre-Alpha",
            parent=menu_ui,
            y=0.12,
            origin=(-1.2, -1),
            scale=2,
            rotation = Vec3(0, 0, 12),
            color=color.blue,
            letter_spacing=2
        )

        self.button_bg = Entity(
            parent=menu_ui,
            model="quad",
            color=color.rgba(0, 0, 0, 120),
            scale=(0.5, 0.25),
            y=-0.05,
            z=1,
            radius=0.2
        )

        btn_play_txt = "ИГРАТЬ"
        btn_quit_txt = "ВЫХОД"

        self.btn_play = MenuButton(text=btn_play_txt, on_click=start_game, y_pos=0.02)
        self.btn_quit = MenuButton(text=btn_quit_txt, on_click=quit_game, y_pos=-0.10)

        self.version_text = Text(
            text="0.1.0-pre-alpha | Developed by PyForge",
            parent=menu_ui,
            position=(0, -0.45),
            origin=(0, 0),
            scale=0.8,
            color=color.blue
        )

        self.particles = []
        for i in range(40):
            p = Entity(
                parent=menu_ui,
                model="sphere",
                color=random.choice([color.blue, color.azure, color.white, color.gray]),
                scale=(0.01, 0.01),
                position=(random.uniform(-0.9, 0.9), random.uniform(-0.4, 0.4)),
                z=5
            )
            self.particles.append(p)

        self.time_counter = 0

    def update(self):
        self.model_pivot.rotation_y += 20 * time.dt

        self.time_counter += time.dt
        float_offset = math.sin(self.time_counter * 1.5) * 0.008
        
        self.title_main.y = 0.25 + float_offset
        self.title_shadow.y = 0.25 + float_offset
        # title_glow.y = 0.25 + float_offset
        
        self.subtitle.y = 0.12 + float_offset * 0.5

        glow_alpha = 40 + math.sin(self.time_counter * 3) * 20
        # title_glow.color = color.rgba(0, 150, 255, int(glow_alpha))
        
        for p in self.particles:
            p.rotation_z += 10 * time.dt
            p.y += math.sin(self.time_counter + p.x) * 0.0005

        camera.look_at(self.model_pivot)
        self.hero_model.rotation_z = math.sin(self.time_counter) * 5
        self.hero_model.rotation_x = math.cos(self.time_counter * 0.5) * 3

    def run(self):
        self.app.run()


if __name__ == "__main__":
    menu = EnduraMenu()
    menu.run()
    