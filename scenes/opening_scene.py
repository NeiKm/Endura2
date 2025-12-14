from ursina import *
from core.ObjectFactory import ObjectFactory
from entities.player import Player
from ursina.shaders import lit_with_shadows_shader

class OpeningScene:
    def __init__(self):
        camera.position = (0, 5, -15)
        camera.look_at((0, 0, 0))
        camera.animate_position((0, 3, -8), duration=1, curve=curve.in_out_cubic)