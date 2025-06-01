from .database import DatabaseConnection
from .settings import Settings

all_settings = Settings()

db_connection = DatabaseConnection(all_settings)
