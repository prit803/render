from sqlalchemy import create_engine ,text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")

def test_postgres_connection():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1;"))  # ✅ wrap in text()
            print("✅ Connection successful:", result.scalar())
    except OperationalError as e:
        print("❌ Connection failed:", str(e))

if __name__ == "__main__":
    test_postgres_connection()