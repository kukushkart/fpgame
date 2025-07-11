import json
import os
from datetime import datetime
class SaveManager:
    def __init__(self):
        self.save_dir = "saves"
        self.save_file = "game_save.json"
        self.save_path = os.path.join(self.save_dir, self.save_file)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    def save_game(self, player, day, wave, money, player_name="", save_name="game_save"):
        save_data = {
            "save_name": save_name,
            "player_name": player_name,
            "day": day,
            "wave": wave,
            "money": money,
            "player": {
                "health": player.health,
                "max_health": player.max_health,
                "damage": player.damage,
                "speed": player.speed,
                "shoot_delay": player.shoot_delay,
                "reload_time": player.reload_time,
                "magazine_size": player.magazine_size,
                "current_ammo": player.current_ammo,
                "medkits": player.medkits,
                "facing_right": player.facing_right,
                "ammo_capacity_bought": player.ammo_capacity_bought,
                "skin_path": player.skin_path
            },
            "timestamp": datetime.now().isoformat()
        }
        safe_name = "".join(c for c in save_name if c.isalnum() or c in (' ', '_', '-')).rstrip()
        save_file = f"{safe_name}.json"
        save_path = os.path.join(self.save_dir, save_file)
        try:
            with open(save_path, 'w') as f:
                json.dump(save_data, f, indent=2)
            print(f"Game saved successfully to {save_path}")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    def load_game(self):
        if not os.path.exists(self.save_path):
            print("No save file found")
            return None
        try:
            with open(self.save_path, 'r') as f:
                save_data = json.load(f)
            print(f"Game loaded successfully from {self.save_path}")
            return save_data
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    def has_save_file(self):
        return os.path.exists(self.save_path)
    def get_save_info(self):
        if not self.has_save_file():
            return None
        try:
            with open(self.save_path, 'r') as f:
                save_data = json.load(f)
            return {
                "save_name": save_data.get("save_name", "Unknown"),
                "player_name": save_data.get("player_name", "Unknown"),
                "day": save_data.get("day", 1),
                "wave": save_data.get("wave", 1),
                "money": save_data.get("money", 0),
                "timestamp": save_data.get("timestamp", "Unknown")
            }
        except Exception as e:
            print(f"Error reading save info: {e}")
            return None
    def get_all_saves(self):
        if not os.path.exists(self.save_dir):
            return []
        saves = []
        for filename in os.listdir(self.save_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.save_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        save_data = json.load(f)
                    saves.append({
                        "filename": filename,
                        "save_name": save_data.get("save_name", filename[:-5]),  
                        "player_name": save_data.get("player_name", "Unknown"),
                        "day": save_data.get("day", 1),
                        "wave": save_data.get("wave", 1),
                        "money": save_data.get("money", 0),
                        "timestamp": save_data.get("timestamp", "Unknown")
                    })
                except Exception as e:
                    print(f"Error reading save file {filename}: {e}")
        saves.sort(key=lambda x: x["timestamp"], reverse=True)
        return saves
    def load_save_by_filename(self, filename):
        filepath = os.path.join(self.save_dir, filename)
        if not os.path.exists(filepath):
            print(f"Save file {filename} not found")
            return None
        try:
            with open(filepath, 'r') as f:
                save_data = json.load(f)
            print(f"Game loaded successfully from {filepath}")
            return save_data
        except Exception as e:
            print(f"Error loading save file {filename}: {e}")
            return None
    def delete_save(self):
        if os.path.exists(self.save_path):
            try:
                os.remove(self.save_path)
                print("Save file deleted successfully")
                return True
            except Exception as e:
                print(f"Error deleting save file: {e}")
                return False
        return False
    def delete_save_by_filename(self, filename):
        filepath = os.path.join(self.save_dir, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"Save file {filename} deleted successfully")
                return True
            except Exception as e:
                print(f"Error deleting save file {filename}: {e}")
                return False
        return False
    def get_save_count(self):
        return len(self.get_all_saves())
    def can_create_save(self):
        return self.get_save_count() < 6
