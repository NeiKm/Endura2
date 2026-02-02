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
                
                match parts[2]:

                    case "texture":
                        pass

                    case "color":
                        pass

                    case "size":
                        pass

                    case "model":
                        pass

            case "rotate":
                pass

            case "delete":
                destroy(self.ent_manager.selected_block)

            case "copy":
                self.copy_selected_entity()

            case _:
                print(f"Неизвестная команда {command}")

    def move_entity(self, pos: Vec3):
        if self.ent_manager.selected_block:
            self.ent_manager.selected_block.position = pos

    def copy_entity(self):
        sel_entity = self.ent_manager.selected_entity

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

        self.ent_manager.selected_entity = new_entity
