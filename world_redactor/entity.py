from ursina import *
import os
from json import dump
import json


class EntityManager:
    def __init__(self):
        self.entities = []
        self.highlighted_block = None
        self.selected_block = None
        self.defolt_block_size = 1
        self.defolt_color = color.white
        self.load_map()

    def add(self, entity):
        self.entities[entity.name] = entity

    def get(self, name):
        return self.entities.get(name)
    
    def highlight_block(self):
        if mouse.hovered_entity and mouse.hovered_entity in self.entities:
            if self.highlighted_block and self.highlighted_block != mouse.hovered_entity:
                self.highlighted_block.color = self.highlighted_block.original_color
            
            self.highlighted_block = mouse.hovered_entity
            if not hasattr(self.highlighted_block, "original_color"):
                self.highlighted_block.original_color = self.highlighted_block.color
            self.highlighted_block.color = color.rgba(255, 255, 0, 150)
        
        elif self.highlighted_block:
            self.highlighted_block.color = self.highlighted_block.original_color
            self.highlighted_block = None

    def save_to_json(self):
        folder = "world_redactor"
        os.makedirs(folder, exist_ok=True)

        save_path = os.path.join(folder, "world.json")

        data_to_save = []

        for ent in self.entities:
            data_to_save.append({
                "model": ent.model.name if hasattr(ent.model, "name") else "cube",

                "position": [ent.x, ent.y, ent.z],
                "rotation": [ent.rotation.x, ent.rotation.y, ent.rotation.z],
                "scale": [ent.scale.x, ent.scale.y, ent.scale.z],

                "texture": ent.texture.name if ent.texture else "white_cube",
                "texture_scale": [ent.texture_scale[0], ent.texture_scale[1]],

                "color": [ent.color.r, ent.color.g, ent.color.b],
                "collider": "box" if ent.collider else None
            })

        try:
            with open(save_path, "w", encoding="utf-8") as save:
                dump(data_to_save, save, indent=4, ensure_ascii=False)

            print(f"Сохранено в: {save_path}")

        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

    def load_map(self, filename="world.json"):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        SAVE_PATH = os.path.join(BASE_DIR, filename)

        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

            for block in data:
                position = Vec3(*block["position"])
                rotation = Vec3(*block["rotation"])
                scale = tuple(block["scale"])

                texture = block.get("texture", "white_cube")
                texture_scale = tuple(block.get("texture_scale", (1, 1)))
                collider = block.get("collider", "box")

                color_data = block.get("color", [1, 1, 1])

                if len(color_data) == 3:
                    color_data.append(1)

                color_val = color.rgba(
                    color_data[0],
                    color_data[1],
                    color_data[2],
                    color_data[3]
                )

                self.create_entity(
                    pos=position,
                    scale=scale,
                    rotation=rotation,
                    texture=texture,
                    texture_scale=texture_scale,
                    color=color_val,
                    collider=collider
                )

        except FileNotFoundError as e:
            print("Файл карты не найден\n>>>", e)

    def create_entity(
        self,
        pos=(0, 0, 0),
        scale=(1, 1, 1),
        rotation=(0, 0, 0),
        texture="white_cube",
        texture_scale=(1, 1),
        color=color.white,
        collider="box"
    ):
        ent = Entity(
            model="cube",
            position=pos,
            rotation=rotation,
            scale=scale,
            texture=texture,
            texture_scale=texture_scale,
            color=color,
            collider=collider
        )

        self.entities.append(ent)
        return ent
