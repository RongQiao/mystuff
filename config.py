import os


class DataBaseConfig(object):
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DB_DIR = os.path.join(self.BASE_DIR, "data")
        self.DB_PATH = os.path.join(self.DB_DIR, "app.db")
        self.SCHEMA_PATH = os.path.join(self.BASE_DIR, "schemas", "finance_income.json")
        self.DATA_FILE_PATH = os.path.join(self.DB_DIR, "sample")


db_config = DataBaseConfig()
