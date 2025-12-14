from ursina import *
from core.settings import *
from ursina.shaders import camera_contrast_shader
from scenes.main_scene import MainScene

def start_game():
    pass

app = Ursina(multisample=True, development_mode=True)

window.title = "Endura2"
window.borderless = False
window.fullscreen = FULLSCREEN
window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
window.color = color.rgb(30, 30, 40)
window.fps_counter.enabled = True
window.fps_counter.position = (0.0, 0.0)

window.collider_helper = True

camera.shader = camera_contrast_shader
camera.set_shader_input('contrast', 1)

sun = DirectionalLight(shadows=True, rotation=(45, -45, 45), shadow_resolution=(2048, 2048))
sun.look_at(Vec3(1, -1, -1))
sun.shadow_map_resolution = Vec2(4096, 4096)
sun.shadow_bias = 0.5

scene_ = MainScene()

menu = Entity(parent=camera.ui)

# Анимация камеры при запуске
start_pos = Vec3(camera.position.x, camera.position.y + 5, camera.position.z - 15)
camera.position = start_pos
camera.animate_position(Vec3(0, 0, 0), duration=2, curve=curve.in_out_cubic)

app.run()
