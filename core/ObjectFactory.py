from ursina import *
from ursina.shaders import lit_with_shadows_shader

class ObjectFactory:
    """
    Класс-фабрика для создания объектов с дефолтными свойствами.
    Инициализируется один раз при импорте сцен.
    """

    def __init__(self):
        self.default_color = color.white
        self.default_scale = 1
        self.default_shader = lit_with_shadows_shader
        self.default_collider = "box"
        self.default_texture_filter = "linear"

    def create_entity(self, **kwargs):
        color_val = kwargs.pop("color", self.default_color)
        scale_val = kwargs.pop("scale", self.default_scale)
        shader_val = kwargs.pop("shader", self.default_shader)
        collider_val = kwargs.pop("collider", self.default_collider)
        texture_filter_val = kwargs.pop("texture_filter", self.default_texture_filter)

        return Entity(
            color=color_val,
            scale=scale_val,
            shader=shader_val,
            collider=collider_val,
            texture_filter = texture_filter_val,
            **kwargs
        )