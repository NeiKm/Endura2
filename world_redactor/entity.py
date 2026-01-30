from ursina import *

class EntityManager:
    def __init__(self):
        self.entities = []
        self.highlighted_block = None
        self.selected_block = None
        self.defolt_block_size = 1
        self.defolt_color = color.white

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

    def create_entity (
        self, pos, 
        scale = (1, 1, 1),
        color = color.white,
        rotation = (0, 0, 0), 
        texture = "white_cube",
        texture_scale = (1, 1)
    ):
        if isinstance(texture, str) and texture != "white_cube":
            texture = self.get_full_texture_path(texture)

        self.ent = Entity(
            model = "cube",
            texture = texture,
            texture_scale = texture_scale,
            rotation = rotation,
            position = pos,
            scale = scale,
            color = color,
            collider = "box"
        )
        self.entities.append(self.ent)
        self.ent.texture_scale = texture_scale
        return self.ent
