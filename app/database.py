from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Step 1: Set your actual PostgreSQL username, password, and database
DATABASE_URL = "postgresql://airport_db_yays_user:yje5ChhPnGChs4CHHf1GfdE2gUssHNzA@dpg-cvq43heuk2gs73csbgeg-a/airport_db_yays"
# Step 2: Create the database engine
engine = create_engine(DATABASE_URL)

# Step 3: Create the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Step 4: Create the base class for table models
Base = declarative_base()

# Step 5: Define the Passenger table
class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String, unique=True)
    queue_number = Column(Integer, unique=True)
    qr_code_path = Column(String)
    checked_in = Column(Boolean, default=False)

# Step 6: Create the table in the database (runs once at startup)
Base.metadata.create_all(bind=engine)