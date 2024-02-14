import os
import sqlite3


class ImageMetaRepository:
    connection = None
    current_path = os.getcwd()
    db_name = "scraped_image_meta.db"
    db_file = os.path.join(current_path, db_name)

    def __init__(self):
        self.open_db_connection()
        self.init_db_schema()

    def open_db_connection(self):
        if os.path.exists(self.db_file):
            self.connection = sqlite3.connect(self.db_file)
        else:
            self.connection = sqlite3.connect(self.db_file)

    def init_db_schema(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS ImageMeta (Id INTEGER PRIMARY KEY AUTOINCREMENT, SourceUrl "
                           "TEXT, Host TEXT, ETag TEXT)")
            cursor.close()
            self.connection.commit()
        except Exception as e:
            print(e)
            raise e

    def is_image_scraped(self, scraped_url) -> bool:
        try:
            cursor = self.connection.cursor()
            row_count = cursor.execute("SELECT COUNT(*) FROM ImageMeta WHERE SourceUrl = ?", (scraped_url,)).fetchone()[0]
            cursor.close()
            self.connection.commit()
            return row_count > 0
        except Exception as e:
            print(e)
            raise e

    def save_image_meta(self, image_url, host, e_tag) -> int:
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO ImageMeta (SourceUrl, Host, ETag) VALUES (?, ?, ?)",
                           (image_url, host, e_tag))
            last_row_id = cursor.lastrowid
            cursor.close()
            self.connection.commit()
            return last_row_id
        except Exception as e:
            print(e)
            raise e

    def get_image_meta(self, scraped_url) -> list:
        try:
            cursor = self.connection.cursor()
            rows = cursor.execute("SELECT * FROM ImageMeta WHERE SourceUrl = ?", scraped_url).fetchall()

            cursor.close()
            self.connection.commit()

            return rows
        except Exception as e:
            print(e)
            raise e

    def close_db_connection(self):
        self.connection.close()
