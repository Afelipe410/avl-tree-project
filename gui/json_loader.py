import json
from gui.avl_tree import AVLTree

def load_game_from_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    config = data.get("config", {})
    obstacles = data.get("obstacles", [])

    avl = AVLTree()
    for obs in obstacles:
        avl.insert(obs["x_world"], obs)

    return config, avl
