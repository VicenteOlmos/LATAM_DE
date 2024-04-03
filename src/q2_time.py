import json
import sqlite3
from typing import List, Tuple
import emoji


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    conn = sqlite3.connect("emojis.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS tweets
                 (content TEXT)"""
    )
    conn.commit()

    c.execute("SELECT COUNT(*) FROM tweets")
    count = c.fetchone()[0]
    if count == 0:
        with open(file_path, "r") as file:
            for line in file:
                tweet = json.loads(line)
                tweet_text = tweet["content"]
                c.execute(
                    "INSERT INTO tweets (content) VALUES (?)",
                    (str(tweet_text),),
                )
        conn.commit()

    query_top_emojis = """ SELECT content FROM tweets"""
    c.execute(query_top_emojis)

    emoji_counter = {}
    for row in c.fetchall():
        tweet = row[0]
        for char in tweet:
            if char in emoji.UNICODE_EMOJI["en"]:
                if char in emoji_counter:
                    emoji_counter[char] += 1
                else:
                    emoji_counter[char] = 1
    conn.close()

    return sorted(emoji_counter.items(), key=lambda x: x[1], reverse=True)[:10]
