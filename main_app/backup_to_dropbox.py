import os
import dropbox
import psycopg2
from datetime import datetime
from dropbox import DropboxOAuth2FlowNoRedirect

# Настройки базы данных
DB_NAME = "course_work"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

# Refresh Token для Dropbox
DROPBOX_REFRESH_TOKEN = "JZT5EmqTH3YAAAAAAAAAAcYeUqpPCe64zNgCVhUPhj7PPe8IFEjxelZccfWliEK4"
APP_KEY = "9ayq9naf8get7nz"
APP_SECRET = "4hkvnvjsgrt15lj"

# Имя файла для экспорта
backup_file = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"

# Функция для подключения к базе данных и выполнения дампа
def export_database_to_file():
    try:
        print("Подключение к базе данных...")
        # Подключение к базе данных
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        print(f"Экспорт базы данных в файл {backup_file}...")
        # Выполнение команды COPY для дампа данных
        with open(backup_file, "w", encoding="utf-8") as f:
            for table_name in get_table_names(cursor):
                cursor.copy_expert(f"COPY {table_name} TO STDOUT WITH CSV HEADER", f)

        cursor.close()
        conn.close()
        print("Экспорт завершён.")
    except Exception as e:
        print(f"Ошибка при экспорте: {e}")
        raise

# Получение списка таблиц
def get_table_names(cursor):
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    return [row[0] for row in cursor.fetchall()]

# Функция загрузки на Dropbox
def upload_to_dropbox():
    try:
        print("Подключение к Dropbox...")
        dbx = dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=DROPBOX_REFRESH_TOKEN)

        print(f"Загрузка файла {backup_file} в Dropbox...")
        with open(backup_file, "rb") as f:
            dbx.files_upload(f.read(), f"/{backup_file}", mode=dropbox.files.WriteMode("overwrite"))

        print(f"Файл успешно загружен в Dropbox: /{backup_file}")
    except Exception as e:
        print(f"Ошибка при загрузке в Dropbox: {e}")
        raise
    finally:
        # Удаление локального файла
        if os.path.exists(backup_file):
            os.remove(backup_file)
            print(f"Локальный файл {backup_file} удалён.")

# Основная функция
def main():
    export_database_to_file()
    upload_to_dropbox()

if __name__ == "__main__":
    main()