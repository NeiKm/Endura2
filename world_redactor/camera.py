from ursina import *

class Camera(Entity):

    def __init__(self, entity, flor, UI):
        super().__init__()
        self.entity = entity
        self.camera_setup()
        self.speed = 20
        self.flor = flor
        self.UI = UI
        self.cmd = self.UI.get_cmd_status()
        camera.fov = 80
        

    def update(self):
        self.cmd = self.UI.get_cmd_status()
        if mouse.locked:
            direction = Vec3(
                int(held_keys['d']) - int(held_keys['a']),
                int(held_keys['space']) - int(held_keys['shift']),
                int(held_keys['w']) - int(held_keys['s'])
            ).normalized() * self.speed * time.dt
            camera.position += camera.forward * direction.z + camera.right * direction.x + Vec3(0, 1, 0) * direction.y
            camera.rotation_x -= mouse.velocity[1] * self.sensitivity
            camera.rotation_y += mouse.velocity[0] * self.sensitivity

            if held_keys["e"]:
                self.entity.selected_block.position += (0, 0.1, 0)
            elif held_keys["q"]:
                self.entity.selected_block.position -= (0, 0.1, 0)

            self.entity.highlight_block()

        else:
            self.entity.highlight_block()

        if held_keys["o"]:
            camera.fov += 1
        elif held_keys["p"]:
            camera.fov -= 1

    def camera_setup(self):
        self.velocity = Vec3(0, 0, 0)
        mouse.locked = False
        self.sensitivity = 50

    def input(self, key):
        print(self.cmd)
        try:
            if not self.cmd:
                if key == "=" and mouse.hovered_entity:
                    pos = mouse.hovered_entity.position + mouse.normal
                    self.entity.selected_block = self.entity.create_entity(
                        pos=pos,
                        scale=(self.entity.defolt_block_size, self.entity.defolt_block_size, self.entity.defolt_block_size), 
                        color=self.entity.defolt_color
                    )
                elif key == "-" and mouse.hovered_entity and mouse.hovered_entity != self.flor:
                    self.entity.entities.remove(mouse.hovered_entity)
                    destroy(mouse.hovered_entity)

                elif key == "scroll up":
                    self.entity.selected_block.scale += Vec3(0.2, 0.2, 0.2)

                elif key == "scroll down":
                    self.entity.selected_block.scale -= Vec3(0.2, 0.2, 0.2)

                elif key == "/":
                    print("scale: ", self.entity.selected_block.scale)
                    print("position: ", self.entity.selected_block.position)

                elif key == "m":
                    self.entity.save_to_json()

                elif key == "z":
                    self.entity.selected_block.rotation += (10, 0, 0)
                elif key == "x":
                    self.entity.selected_block.rotation += (0, 10, 0)
                elif key == "c":
                    self.entity.selected_block.rotation += (0, 0, 10)

                elif key == "5":
                    self.entity.selected_block.scale += (0.25, 0, 0)
                elif key == "6":
                    self.entity.selected_block.scale += (0, 0.25, 0)
                elif key == "7":
                    self.entity.selected_block.scale += (0, 0, 0.25)

                elif key == "8":
                    self.entity.selected_block.scale -= (0.25, 0, 0)
                elif key == "9":
                    self.entity.selected_block.scale -= (0, 0.25, 0)
                elif key == "0":
                    self.entity.selected_block.scale -= (0, 0, 0.25)

                elif key == "up arrow":
                    self.entity.selected_block.position += (0, 0, 0.5)
                elif key == "down arrow":
                    self.entity.selected_block.position += (0, 0, -0.5)
                elif key == "left arrow":
                    self.entity.selected_block.position += (-0.5, 0, 0)
                elif key == "right arrow":
                    self.entity.selected_block.position += (0.5, 0, 0)

                if key == "left mouse down" and mouse.hovered_entity:
                    if mouse.hovered_entity in self.entity.entities:
                        self.entity.selected_block = mouse.hovered_entity
                        print(f"выбран блок: {self.entity.selected_block}")

                if key == "right mouse down":
                    mouse.locked = not mouse.locked
                    
        except Exception as e:
            print(f"Ошибка: {e}")
            self.entity.selected_block = None
                