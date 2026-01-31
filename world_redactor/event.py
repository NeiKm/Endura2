from ursina import *

class Event:
    
    def __init__(self, scene):
        self.scene = scene

    def delete_entity(self, name):
        destroy(self.scene.get_entity(name))


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
                pass

            case "copy":
                pass

            case _:
                print(f"Неизвестная кмда {command}")

    def move_entity(self, pos: Vec3):
        print(self.ent_manager.selected_block)
        if self.ent_manager.selected_block:
            self.ent_manager.selected_block.position = pos
