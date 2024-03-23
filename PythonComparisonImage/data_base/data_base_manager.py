import psycopg2
import os


class DatabaseManager:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Соединение с базой данных успешно установлено")
        except psycopg2.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Соединение с базой данных закрыто")

    def create_original_image_table(self):
        if self.connection:
            try:
                query = '''
                CREATE TABLE IF NOT EXISTS original_images (
                    id SERIAL PRIMARY KEY,
                    image_name VARCHAR(255) NOT NULL,
                    image_data BYTEA NOT NULL
                )
                '''
                self.cursor.execute(query)
                self.connection.commit()
                print("Таблица original_images успешно создана")
            except psycopg2.Error as e:
                print(f"Ошибка при создании таблицы original_images: {e}")

    def create_comparison_image_table(self):
        if self.connection:
            try:
                query = '''
                CREATE TABLE IF NOT EXISTS comparison_images (
                    id SERIAL PRIMARY KEY,
                    id_original_image INTEGER NOT NULL REFERENCES original_images(id),
                    image_name VARCHAR(255) NOT NULL,
                    image_data BYTEA NOT NULL
                )
                '''
                self.cursor.execute(query)
                self.connection.commit()
                print("Таблица comparison_images успешно создана")
            except psycopg2.Error as e:
                print(f"Ошибка при создании таблицы comparison_images: {e}")

    def insert_original_image(self, path_to_image):
        image_name = os.path.basename(path_to_image)

        with open(path_to_image, "rb") as f:
            image_data = f.read()

        if self.connection is not None:
            cursor = self.connection.cursor()
            try:
                insert_query = '''
                    INSERT INTO original_images (image_name, image_data) VALUES (%s, %s)
                    '''
                cursor.execute(insert_query, (image_name, psycopg2.Binary(image_data)))
                self.connection.commit()
                print("Изображение успешно вставлено в таблицу")
            except psycopg2.Error as e:
                print(f"Ошибка при вставке изображения: {e}")

    def select_all(self):
        if self.connection:
            try:
                query = f"SELECT * FROM original_images;"
                self.cursor.execute(query)
                rows = self.cursor.fetchall()

                for row in rows:
                    print(row)

            except psycopg2.Error as e:
                print(f"Ошибка при выполнении запроса: {e}")

    def execute_query(self, query):
        if self.connection:
            try:
                self.cursor.execute(query)
                self.connection.commit()
                print("Запрос успешно выполнен")
            except psycopg2.Error as e:
                print(f"Ошибка при выполнении запроса: {e}")