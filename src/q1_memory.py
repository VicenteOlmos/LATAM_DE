from typing import List, Tuple
from datetime import datetime
import json


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    class BSTNode:
        def __init__(self, date, user):
            self.date = date
            self.users = {user: 1}
            self.left = None
            self.right = None

        def insert(self, date, user):
            if date < self.date:
                if self.left is None:
                    self.left = BSTNode(date, user)
                else:
                    self.left.insert(date, user)
            elif date > self.date:
                if self.right is None:
                    self.right = BSTNode(date, user)
                else:
                    self.right.insert(date, user)
            else:
                if user in self.users:
                    self.users[user] += 1
                else:
                    self.users[user] = 1

        def get_top_users(self):
            data = []
            if self.left:
                data.extend(self.left.get_top_users())
            data.append(
                (
                    self.date,
                    max(self.users, key=self.users.get),
                    sum(self.users.values()),
                )
            )
            if self.right:
                data.extend(self.right.get_top_users())
            return data

    root = None
    try:
        with open(file_path, "r") as file:
            for line in file:
                try:
                    tweet = json.loads(line)
                    date = datetime.fromisoformat(tweet["date"]).date()
                    user = tweet["user"]["username"]
                    if root is None:
                        root = BSTNode(date, user)
                    else:
                        root.insert(date, user)
                except json.JSONDecodeError:
                    print("Error al decodificar JSON.")
                    continue
    except FileNotFoundError:
        print(f"El archivo {file_path} no existe.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

    all_data = root.get_top_users() if root else []
    top_dates = sorted(all_data, key=lambda x: x[2], reverse=True)[:10]
    return [(date, user) for date, user, _ in top_dates]