import json
from gui.avl_tree import AVLTree

def load_game_from_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    config = data.get("config", {})
    obstacles = data.get("obstacles", [])

    avl = AVLTree()
    for obs in obstacles:
        # La clave es una tupla (x_world, lane_idx)
        key = (obs["x_world"], obs["lane_idx"])
        avl.insert(key, obs)

    return config, avl
