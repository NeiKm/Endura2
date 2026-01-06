import json
import copy

DEFAULT_SETTINGS = {
    "graphics": {
        "fullscreen": False,
        "resolution": [1280, 720],
        "vsync": True,
        "fps_limit": 60,

        "texture_quality": "high",
        "shadows": True,
        "shadow_quality": "medium",
        "shadow_res": 2048,

        "aa": True,
        "anisotropy": 8,

        "brightness": 1.0,
        "gamma": 1.0,
    },

    "audio": {
        "master": 1.0,
        "music": 0.7,
        "sfx": 0.8,
        "ui": 0.6,
        "mute": False,
    },

    "controls": {
        "mouse_sens": 1.0,
        "invert_y": False,
        "keys": {
            "forward": "w",
            "back": "s",
            "left": "a",
            "right": "d",
            "jump": "space",
            "interact": "e",
        }
    },

    "gameplay": {
        "difficulty": "normal",
        "autosave": True,
        "autosave_time": 300,
        "tutorial": True,
    },

    "ui": {
        "language": "ru",
        "show_fps": True,
        "scale": 1.0,
    }
}

def load_settings(path="settings.json"):
    settings = copy.deepcopy(DEFAULT_SETTINGS)

    try:
        with open(path, "r", encoding="utf-8") as f:
            user = json.load(f)
        print("USER SETTINGS:", user)  # ← Уже не важно ;o
        merge(settings, user)

    except Exception:
        pass
    
    return settings


def merge(base, custom):
    for k, v in custom.items():
        if isinstance(v, dict) and k in base:
            merge(base[k], v)
        else:
            base[k] = v
