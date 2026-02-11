from ursina import *
from ursina.shaders import lit_with_shadows_shader
import json
import os


class LoadMap():
    def __init__(self):
        pass

    def load_map(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Файл мира не найдн: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        created_entities = []

        for obj in data:
            position = Vec3(*obj.get("position", [0, 0, 0]))
            rotation = Vec3(*obj.get("rotation", [0, 0, 0]))
            scale    = Vec3(*obj.get("scale",    [1, 1, 1]))

            col = obj.get("color", [1.0, 1.0, 1.0])

            color_val = color.rgb(float(col[0]), float(col[1]), float(col[2]))

            entity = Entity(
                model=obj.get("model", "cube"),
                position=position,
                rotation=rotation,
                scale=scale,
                texture=obj.get("texture", None),
                color=color_val,
                collider=obj.get("collider", None),
                shader = lit_with_shadows_shader
            )

            created_entities.append(entity)

        return created_entities
    