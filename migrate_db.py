from app.infrastructure.db.database import Base, engine, SessionLocal
from sqlalchemy import text

def migrate():
    # Oddiy migration: ustun qo'shish
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS business_type VARCHAR(100)"))
            conn.commit()
            print("Migration successful: business_type added")
    except Exception as e:
        print(f"Migration error: {e}")

if __name__ == "__main__":
    migrate()
