from ursina import *
from core.settings import *
from ursina.shaders import camera_contrast_shader
from settings import load_settings
from scenes.main_scene import MainScene


class Main:
    def __init__(self):
        self.SETTINGS = load_settings()
        self.app = Ursina(multisample=True, development_mode=True)

        self.setup_window()
        self.setup_camera()
        self.setup_light()
        self.scene = MainScene()
        self.menu = Entity(parent=camera.ui)
        self.animate_camera_start()

    def setup_window(self):
        window.title = "Endura2"
        window.borderless = False
        window.fullscreen = True if self.SETTINGS == "true" else False
        window.size = (self.SETTINGS["graphics"]["resolution"][0], self.SETTINGS["graphics"]["resolution"][1])
        window.color = color.rgb(30, 30, 40)
        window.fps_counter.enabled = True
        window.fps_counter.position = (0.0, 0.0)
        window.collider_helper = True

    def setup_camera(self):
        camera.shader = camera_contrast_shader
        camera.set_shader_input('contrast', 1)

    def setup_light(self):
        sun = DirectionalLight(
            shadows=True,
            rotation=(45, -45, 45),
            shadow_resolution=(2048, 2048)
        )
        sun.look_at(Vec3(1, -1, -1))
        sun.shadow_map_resolution = Vec2(4096, 4096)
        sun.shadow_bias = 0.5

    def animate_camera_start(self):
        start_pos = Vec3(camera.position.x, camera.position.y + 5, camera.position.z - 15)
        camera.position = start_pos
        camera.animate_position(Vec3(0, 0, 0), duration=2, curve=curve.in_out_cubic)

    def run(self):
        self.app.run()

if __name__ == "__main__":
    print(
        "Этот файл нельзя запускать напрямую.\n"
        "Для корректной работы, запускайте игру через launcher.py"
    )
    exit(1)
