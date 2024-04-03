import json
from typing import List, Tuple
import emoji


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    class BSTNode:
        def __init__(self, emoji):
            self.emoji = emoji
            self.counter = 1
            self.left = None
            self.right = None

        def insert(self, emoji):
            if emoji < self.emoji:
                if self.left is None:
                    self.left = BSTNode(emoji)
                else:
                    self.left.insert(emoji)
            elif emoji > self.emoji:
                if self.right is None:
                    self.right = BSTNode(emoji)
                else:
                    self.right.insert(emoji)
            else:
                self.counter += 1

        def get_top_emojis(self):
            data = []
            if self.left:
                data.extend(self.left.get_top_emojis())
            data.append((self.emoji, self.counter))
            if self.right:
                data.extend(self.right.get_top_emojis())
            return data

    root = None
    try:
        with open(file_path, "r") as file:
            for line in file:
                try:
                    tweet = json.loads(line)
                    for char in tweet["content"]:
                        if char in emoji.UNICODE_EMOJI["en"]:
                            if root is None:
                                root = BSTNode(char)
                            else:
                                root.insert(char)
                except json.JSONDecodeError:
                    print("Error al decodificar JSON.")
                    continue
    except FileNotFoundError:
        print(f"El archivo {file_path} no existe.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []    

    all_data = root.get_top_emojis() if root else []
    return sorted(all_data, key=lambda x: x[1], reverse=True)[:10]