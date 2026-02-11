from ursina import *
from entity import EntityManager

class Event:
    def __init__(self, scene):
        self.scene = scene


class CommandHandler:

    def __init__(self, scene, ent_manager):
        self.ent_manager = ent_manager
        self.scene = scene

    def processing_command(self, command: str):

        if not command:
            return

        parts = command.split()

        match parts[0]:

            case "move":

                self.move_entity(
                    pos=Vec3(float(parts[1]), float(parts[2]), float(parts[3]))
                )

            case "exit":
                application.quit()
            
            case "set":
                
                match parts[1]:

                    case "texture":
                        self.ent_manager.selected_block.texture = str(parts[2])

                    case "color":
                        print(self.ent_manager.selected_block.scale)
                        self.ent_manager.selected_block.color = Color(float(parts[2]), float(parts[3]), float(parts[4]), 1.0)
                        self.ent_manager.selected_block.original_color = Color(float(parts[2]), float(parts[3]), float(parts[4]), 1.0)

                    case "color_a":
                        self.ent_manager.selected_block.color = Color(float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5]))
                        self.ent_manager.selected_block.original_color = Color(float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5]))

                    case "size":
                        self.ent_manager.selected_block.scale = Vec3(float(parts[2]), float(parts[3]), float(parts[4]))

                    case "model":
                        self.ent_manager.selected_block.model = str(parts[2])

            case "rotate":
                self.rotate_entity(
                    rot = Vec3(float(parts[1]), float(parts[2]), float(parts[3]))
                )

            case "delete":
                destroy(self.ent_manager.selected_block)

            case "copy":
                self.copy_entity()

            case _:
                print(f"Неизвестная команда {command}")

    def move_entity(self, pos: Vec3):
        self.ent_manager.selected_block.position = pos

    def rotate_entity(self, rot: Vec3):
        self.ent_manager.selected_block.rotation = rot

    def copy_entity(self):
        sel_entity = self.ent_manager.selected_block

        new_entity = self.ent_manager.create_entity(
            pos=sel_entity.position,
            scale=sel_entity.scale,
            rotation=sel_entity.rotation,
            texture=sel_entity.texture,
            texture_scale=sel_entity.texture_scale,
            color=sel_entity.color,
            collider=sel_entity.collider
        )
        new_entity.y += sel_entity.scale.y

        self.ent_manager.selected_block= new_entity
