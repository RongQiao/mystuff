from pathlib import Path

class DataBaseConfig:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent
        self.DB_DIR = self.BASE_DIR / "data"
        self.DB_PATH = self.DB_DIR / "app.db"
        self.SCHEMA_PATH = self.BASE_DIR / "schemas"
        self.DATA_FILE_PATH = self.DB_DIR / "sample"


db_config = DataBaseConfig()
