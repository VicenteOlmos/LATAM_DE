import json
import re
import sqlite3
from typing import List, Tuple

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    conn = sqlite3.connect("mentions.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS mentions
                 (user TEXT)"""
    )
    conn.commit()

    c.execute("SELECT COUNT(*) FROM mentions")
    count = c.fetchone()[0]
    if count == 0:
        try:
            with open(file_path, "r") as file:
                for line in file:
                    try:
                        tweet = json.loads(line)
                        tweet_text = tweet["content"]
                        mentions = re.findall(r"@(\w+)", tweet_text)
                        for mention in mentions:
                            c.execute(
                                "INSERT INTO mentions (user) VALUES (?)",
                                (mention,),
                            )
                    except json.JSONDecodeError:
                        print("Error al decodificar JSON.")
                        continue
            conn.commit()
        except FileNotFoundError:
            print(f"El archivo {file_path} no existe.")
            return []
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return []
        

    query_most_mentioned = """ SELECT user,COUNT(*) as counter FROM mentions GROUP BY user ORDER BY counter DESC LIMIT 10"""
    c.execute(query_most_mentioned)

    most_mentioned = c.fetchall()
    conn.close()
        
    return most_mentioned