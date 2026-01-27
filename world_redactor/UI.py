from ursina import *

class UI(Entity):

    def __init__(self, command_handler, path):
        super().__init__()
        self.command_handler = command_handler
        self.cmd = False
        self.path = path
        self.input_ = None

    def get_cmd_status(self):
        return self.cmd

    def cmd_show(self):
        if not self.cmd:
            self.input_ = InputField(
                scale=(1.5, .9),
                default_value=self.path,
                max_lines = 10,
                text_color=color.white
            )
        else:
            destroy(self.input_)
        
        self.cmd = not self.cmd


    def update(self):
        if self.cmd:
            if self.input_.text and held_keys["f5"]:
                self.command_handler.check_command(self.input_.text)
                self.input.text = ""

    def input(self, key):
        if key == "alt":
            self.cmd_show()

