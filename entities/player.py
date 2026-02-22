from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import math

class Player(FirstPersonController):

    def __init__(self):
        super().__init__()
        self.player_model = Entity(
            parent=self,
            y=1,
            z=-0.2,
            scale=2,
            rotation_y=-90,
            model="static/3d_model/Player.glb",
            shader = lit_with_shadows_shader,
            cast_shadows=True,
            receive_shadows=True
        )

        self.item_data = {
            "Key": {
                "model": "static/3d_model/key.obj",
                "scale": (0.1, 0.1, 0.3),
                "rotation": (0, 180, -45),
                "position": (0.5, -0.35)
            },
            "Secret Key": {
                "model": "static/3d_model/secret_key.obj",
                "scale": (0.2, 0.2, 0.6),
                "rotation": (0, 180, -45),
                "position": (0.5, -0.35)
            }
        }

        self.hand = Entity(
            parent=camera.ui,
            color=color.yellow,
            model=None,
            scale=(0, 0, 0),
            rotation=(0, 0, 0),
            position=(0, 0)
        )

        # -------------------параметры игрока-------------------
        self.position = (0, -1, 0)
        self.cursor.visible = True
        self.cursor.scale = 0.004
        self.cursor.model = "circle"
        self.cursor.color = color.green
        self.speed = 5
        self.gravity = 0.5
        self.jump_height = 2
        self.camera_pivot.y = 1.85
        self.fly_mode = [self.gravity, False]

        # -------------------состаяние граз-------------------
        self.eye_height = 1.01
        self.eye_state = "closed"
        self.eye_animating = False

        self.top_eye = Entity(
            parent=camera.ui,
            model="quad",
            color=color.black,
            scale=(2, self.eye_height),
            position=(0, 0.5),
            z=-1
        )

        self.bottom_eye = Entity(
            parent=camera.ui,
            model="quad",
            color=color.black,
            scale=(2, self.eye_height),
            position=(0, -0.5),
            z=-1
        )
        # invoke(self.wake_up, delay=0.1)

        # -------------------параметры диалога-------------------
        self.dialog_fill_text = "asdadasdasdasda"
        self.dialog_text = ""
        self.dialog = False
        self.text_index = 0
        self.text_speed = 0.2
        self.dialog_ui = Text(
            text="",
            parent=camera.ui,
            scale=3,
            color=color.black,
            origin=(0, 0),
            position=(0, -0.3),
            enabled=False # включить/отключить видимость субтитров False/True
        )

        self.shake_timer = 0
        self.shake_power = 0.06
        self.shake_speed = 12

        # -------------------параметры стамины и бега-------------------
        self.stamina = 100
        self.max_stamina = 100

        self.stamina_drain = 25
        self.stamina_regen = 15
        self.stamina_regen_delay = 1

        self.can_run = True
        self.last_run_time = 0

        self.last_stamina_value = self.stamina
        self.stamina_visible_timer = 0
        self.stamina_fade_delay = 1

        self.stamina_bar_bg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.gray,
            scale=(0.4, 0.03),
            position=(0, -0.45)
        )

        self.stamina_bar = Entity(
            parent=self.stamina_bar_bg,
            model='quad',
            color=color.blue,
            scale=(1, 1),
            position=(-0.5, 0),
            origin=(-0.5, 0)
        )
        self.stamina_bar_bg.alpha = 0
        self.stamina_bar.alpha = 0

        #-------------------параметры инвентаря-------------------

        self.inventory_open = False
        self.inventory_slots = 8
        self.inventory = []

        self.inventory_ui = Entity(
            parent=camera.ui,
            enabled=False
        )

        self.inventory_bg = Entity(
            parent=self.inventory_ui,
            model='quad',
            color=color.rgba(20,20,20,220),
            scale=(0.6, 0.6),
            position=(0, 0)
        )
        self.inventory_bg.alpha = 0.5

        self.inventory_title_bg = Entity(
            parent=self.inventory_ui,
            model='quad',
            color=color.dark_gray,
            scale=(0.3, 0.08),
            position=(0, 0.35)
        )

        self.inventory_title_text = Text(
            text="Inventory",
            parent=self.inventory_ui,
            origin=(0, 0),
            scale=2,
            color=color.white,
            position=(0, 0.35),
            z=-0.1
        )

        self.slot_entities = []

        for i in range(self.inventory_slots):
            row = i // 4
            col = i % 4
            
            slot_pos = (-0.22 + col * 0.15, 0.2 - row * 0.15)

            slot = Entity(
                parent=self.inventory_ui,
                model='quad',
                color=color.gray,
                scale=(0.12, 0.12),
                position=slot_pos,
                z=0
            )

            slot.collider = 'box'
            slot.slot_index = i
            slot.on_click = lambda s=slot: self.select_item_from_slot(s.slot_index)

            slot.text = Text(
                parent=self.inventory_ui,
                text="",
                origin=(0, 0),
                scale=1,
                color=color.white,
                position=slot_pos,
                z=-0.1  
            )

            self.slot_entities.append(slot)

    def toggle_inventory(self):
        self.inventory_open = not self.inventory_open
        self.inventory_ui.enabled = self.inventory_open


    def add_item(self, item_name):
        if len(self.inventory) >= self.inventory_slots:
            print("Инвентарь заполнен")
            return False

        self.inventory.append(item_name)
        self.update_inventory_ui()
        print(f"Добавлен предмет: {item_name}")
        return True


    def remove_item(self, item_name):
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            self.update_inventory_ui()
            print(f"Удалён предмет: {item_name}")
            return True

        print("Предмет не найден")
        return False


    def update_inventory_ui(self):
        for i in range(self.inventory_slots):
            if i < len(self.inventory):
                self.slot_entities[i].text.text = self.inventory[i]
            else:
                self.slot_entities[i].text.text = ""

    def select_item_from_slot(self, index):
        if index < len(self.inventory):
            item_name = self.inventory[index]
            
            if item_name in self.item_data:
                data = self.item_data[item_name]
                
                self.hand.model = data["model"]
                self.hand.scale = data["scale"]
                self.hand.rotation = data["rotation"]
                self.hand.position = data["position"]
            else:
                self.hand.model = None

    def update(self):
        super().update()

        ray = self.shoot_ray()
        if ray.hit:
            print("Entity---------------------------------------------:", ray.entity.position)

        if self.dialog:
            self.dialog_ui.enabled = True

            if self.text_index < len(self.dialog_fill_text):
                self.text_index += self.text_speed
                self.dialog_ui.text = self.dialog_fill_text[:int(self.text_index)]
        else:
            self.dialog_ui.enabled = False

        if held_keys["e"]:
            self.position += Vec3(0, 0.5, 0)  
        if held_keys["q"]:
            self.position -= Vec3(0, 0.5, 0)  

        if not self.fly_mode[1]:
            is_moving = self.direction.length() > 0 and self.grounded
            running = held_keys["shift"] and is_moving and self.can_run

            if running:
                self.speed = 10
                self.stamina -= self.stamina_drain * time.dt
                self.last_run_time = time.time()

                if self.stamina <= 0:
                    self.stamina = 0
                    self.can_run = False

            else:
                self.speed = 5

            if not running:
                if time.time() - self.last_run_time > self.stamina_regen_delay:
                    self.stamina += self.stamina_regen * time.dt
                    if self.stamina >= self.max_stamina:
                        self.stamina = self.max_stamina
                        self.can_run = True

        self.UI(held_keys["shift"])


    def shoot_ray(self, distance=100):
        return raycast(
            self.camera_pivot.world_position,
            self.camera_pivot.forward,
            distance=distance,
            ignore=(self,)
        )

    def input(self, key):
        super().input(key)

        if key == "alt":
            mouse.locked = not mouse.locked
            self.cursor.visible = not self.cursor.visible
        if key == 'c':
            if self.eye_state == "open":
                self.close_eyes()
                self.add_item("Key")
                
            else:
                self.open_eyes()
                self.add_item("Secret Key") 

        if key == "tab":
            mouse.locked = not mouse.locked
            self.cursor.visible = not self.cursor.visible
            self.toggle_inventory()


        if key == "r":
            self.dialog = not self.dialog
            if self.dialog:
                self.text_index = 0
                self.dialog_ui.text = ""

        if key == "f":
            self.fly_mode[1] = not self.fly_mode[1]
            if self.fly_mode[1]:
                self.gravity = 0
                self.speed = 20
            elif not self.fly_mode[1]:
                self.speed = 5
                self.gravity = self.fly_mode[0]

        if key == "l":
            self.gravity = -1


    def camera_shaking(self):
        is_moving = self.direction.length() > 0 and self.grounded

        if is_moving:
            current_shake_speed = self.shake_speed * 1.5 if held_keys['shift'] else self.shake_speed
            self.shake_timer += time.dt * current_shake_speed

            camera.x = math.cos(self.shake_timer * 0.5) * self.shake_power * 0.5
            camera.y = math.sin(self.shake_timer) * self.shake_power
        else:
            self.shake_timer = 0
            camera.x = lerp(camera.x, 0, time.dt * 10)
            camera.y = lerp(camera.y, 0, time.dt * 10)


    def wake_up(self, with_blink=True, duration=2):
        camera.fov = 120
        camera.animate("fov", 90, duration=2, curve=curve.out_quad)
    
        invoke(self.open_eyes, delay=0.4, duration=duration)
    
        if with_blink:
            invoke(self.blink, delay=1.2)


    def blink(self, duration=0.15):
        if self.eye_animating:
            return

        self.close_eyes(duration)
        invoke(self.open_eyes, delay=duration + 0.02)


    def dialogue_subtitles(self, full_text):
        self.dialog_fill_text = full_text
        self.text_index = 0
        self.dialog_ui.text = ""
        self.dialog = True


    def UI(self, trying_to_run=False):
        percent = self.stamina / self.max_stamina
        self.stamina_bar.scale_x = percent

        if trying_to_run or self.stamina < self.max_stamina:
            self.stamina_visible_timer = 0
            self.stamina_bar_bg.alpha = 1
            self.stamina_bar.alpha = 1
        else:
            self.stamina_visible_timer += time.dt

            if self.stamina_visible_timer > self.stamina_fade_delay:
                self.stamina_bar_bg.alpha = lerp(self.stamina_bar_bg.alpha, 0, time.dt * 4)
                self.stamina_bar.alpha = lerp(self.stamina_bar.alpha, 0, time.dt * 4)


    def _animate_eyes(self, target_scale, duration):
        self.eye_animating = True
        self.target_eye_scale = target_scale

        self.top_eye.animate(
            "scale_y",
            target_scale,
            duration=duration,
            curve=curve.out_expo
        )

        self.bottom_eye.animate(
            "scale_y",
            target_scale,
            duration=duration,
            curve=curve.out_expo
        )

        invoke(self._finish_eye_animation, delay=duration)


    def _finish_eye_animation(self):
        self.eye_animating = False
        self.eye_state = "open" if self.target_eye_scale == 0 else "closed"


    def open_eyes(self, duration=0.4):
        if self.eye_animating or self.eye_state == "open":
            return

        self._animate_eyes(0, duration)


    def close_eyes(self, duration=0.4):
        if self.eye_animating or self.eye_state == "closed":
            return

        self._animate_eyes(self.eye_height, duration)
