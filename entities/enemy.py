from ursina import *
from ursina.physics import raycast


class Monster(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(
            model="sphere",
            color=color.red,
            scale=(1, 2),
            collider="box",
            **kwargs
        )

        self.player = player
        self.speed = 3
        self.stop_distance = 1.5
        self.gravity = 1
        self.grounded = False
        self.game_over = False

    def update(self):
        if not self.player or self.game_over:
            return
        
        target_y = Vec3(0, 1.5, 0)

        direction = self.player.position + target_y - self.position
        distance = direction.length()

        vision_ray = raycast(
            self.world_position,
            direction.normalized(),
            distance=distance,
            ignore=(self,)
        )

        can_see_player = vision_ray.entity == self.player
        
        current_speed = self.speed if can_see_player else self.speed * 1.5

        if distance > self.stop_distance:
            direction = direction.normalized()

            self.look_at(self.player.position + target_y)

            self.position += direction * current_speed * time.dt
            direction.y = 0

        self.apply_gravity()

        if self.intersects(self.player).hit:
            exit()

    def trigger_game_over(self):
        if self.game_over:
            return

        self.game_over = True
        self.player.enabled = False

        camera.fade_out(duration=1.5)

        Text(
            parent=camera.ui,
            text="ТЕБЯ ПОГЛОТИЛА КРАСНАЯ ОШИБКА\n\nGame Over",
            origin=(0, 0),
            scale=2,
            color=color.red,
            background=True
        )

        invoke(application.quit, delay=3)

    def apply_gravity(self):
        ray = raycast(
            self.world_position,
            Vec3(0, -1, 0),
            distance=1.1,
            ignore=(self,)
        )

        if ray.hit:
            self.grounded = True
        else:
            self.y -= self.gravity * time.dt
