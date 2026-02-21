from ursina import *
import subprocess
import os
import sys
import random

app = Ursina()

if random.random() > 0.66:
    model = Entity(model='static/3d_model/key.obj', color=color.yellow, scale=3)
elif random.random() < 0.33:
    model = Entity(model='static/3d_model/Secret_key.obj', color=color.yellow, scale=3)
else:
    model = Entity(model='static/3d_model/Player.glb', scale=3)

pivot = Entity()
camera.parent = pivot
camera.z = -20  

def update():
    pivot.rotation_y += 15 * time.dt
    camera.look_at(model)

def start_game(): 
    subprocess.Popen([sys.executable, "main.py"])
    app.quit() 

menu_parent = Entity(parent=camera.ui)

Button(
    text='Play',
    text_color=color.white,
    color=color.black,
    scale=(0.2, 0.1),
    parent=menu_parent,
    on_click=start_game
)

Text(text='Endura', parent=menu_parent, y=0.3, origin=(0,0), scale=2)

app.run()