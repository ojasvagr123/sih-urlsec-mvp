import os
from sqlmodel import SQLModel, create_engine, Session

# Get the DATABASE_URL from Render or environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://urlsec_db_user:y9pGg6IiyroFtbDZy4XRlghSh2vsXxam@dpg-d3npp3adbo4c73d6r0ig-a/urlsec_db"
)

# Ensure compatibility with SQLAlchemy/Postgres driver
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Fallback (for local dev only)
if not DATABASE_URL:
    DB_PATH = os.environ.get("DB_PATH", "data/app.db")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create the engine
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    """Create all tables if they don't exist."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Return a new database session."""
    return Session(engine)
