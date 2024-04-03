import json
import sqlite3
from typing import List, Tuple
from datetime import datetime


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    conn = sqlite3.connect("tweets.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS tweets
                 (date TEXT, user TEXT, tweet TEXT)"""
    )
    conn.commit()

    c.execute("SELECT COUNT(*) FROM tweets")
    count = c.fetchone()[0]
    if count == 0:
        try:
            with open(file_path, "r") as file:
                for line in file:
                    try:
                        tweet = json.loads(line)
                        date = tweet["date"][:10]
                        user = tweet["user"]["username"]
                        tweet_text = tweet["content"]
                        c.execute(
                            "INSERT INTO tweets (date, user, tweet) VALUES (?, ?, ?)",
                            (date, user, tweet_text),
                        )
                        conn.commit()
                    except json.JSONDecodeError:
                        print("Error al decodificar JSON.")
                        continue
        except FileNotFoundError:
            print(f"El archivo {file_path} no existe.")
            return []
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return []

    query_top_dates = """
    SELECT date
    FROM tweets
    GROUP BY date
    ORDER BY COUNT(*) DESC
    LIMIT 10
    """
    c.execute(query_top_dates)
    top_dates = [row[0] for row in c.fetchall()]

    top_users_per_date = []
    for date in top_dates:
        query_top_user = f"""
        SELECT user, COUNT(*) as tweet_count
        FROM tweets
        WHERE date = '{date}'
        GROUP BY user
        ORDER BY tweet_count DESC
        LIMIT 1
        """
        c.execute(query_top_user)
        top_user,_ = c.fetchone()
        top_users_per_date.append(
            (datetime.strptime(date, "%Y-%m-%d").date(), top_user)
        )
    conn.close()

    return top_users_per_date