import json
import re
from typing import List, Tuple

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    class BSTNode:
        def __init__(self, user):
            self.user = user
            self.counter = 1
            self.left = None
            self.right = None

        def insert(self, user):
            if user < self.user:
                if self.left is None:
                    self.left = BSTNode(user)
                else:
                    self.left.insert(user)
            elif user > self.user:
                if self.right is None:
                    self.right = BSTNode(user)
                else:
                    self.right.insert(user)
            else:
                self.counter += 1

        def get_most_mentioned(self):
            data = []
            if self.left:
                data.extend(self.left.get_most_mentioned())
            data.append((self.user, self.counter))
            if self.right:
                data.extend(self.right.get_most_mentioned())
            return data

    root = None
    try:
        with open(file_path, "r") as file:
            for line in file:
                try:
                    tweet = json.loads(line)
                    tweet_text = tweet["content"]
                    mentions = re.findall(r"@(\w+)", tweet_text)
                    for mention in mentions:
                        if root is None:
                            root = BSTNode(mention)
                        else:
                            root.insert(mention)
                except json.JSONDecodeError:
                    print("Error al decodificar JSON.")
                    continue
    except FileNotFoundError:
        print(f"El archivo {file_path} no existe.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

    all_data = root.get_most_mentioned() if root else []
    return sorted(all_data, key=lambda x: x[1], reverse=True)[:10]