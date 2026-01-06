"""Файл для тестов игры, или мини идей ;)"""

from settings import load_settings

SETTINGS = load_settings()
print(SETTINGS["graphics"]["fullscreen"])
