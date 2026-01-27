from ursina import *
from event import CommandHandler, Event
from UI import UI
from render import Rendering
from entity import EntityManager
from camera import Camera
from pathlib import Path


class Main:

    def __init__(self):
        self.path = str(Path(__file__).resolve())
        self.scene = Ursina(multisample=True, development_mode=True)
        self.rendering = Rendering()
        self.command = CommandHandler(self.scene)
        self.ui = UI(self.command, self.path)
        self.cmd = self.ui.get_cmd_status()
        self.event = Event(self.scene)
        self.ent_man = EntityManager()
        self.camera = Camera(self.ent_man, self.rendering.flor, self.ui)

    def draw_scene(self):
        self.rendering.flor()

    def setup_window(self):
        window.entity_counter.enabled = True
        window.collider_counter.enabled = True
        window.title = "Endura2WorldEditor"
        window.fps_counter.enabled = True

    def run(self):
        self.setup_window()
        self.draw_scene()
        self.scene.run()

if __name__ == "__main__":
    world_redactor = Main()
    world_redactor.run()
