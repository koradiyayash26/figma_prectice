from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True, autoincrement=True)
    token_id = Column(String, nullable=False)
    vs_token_symbol = Column(String, nullable=False)
    swap_value = Column(Float, nullable=False)
    price = Column(Float, nullable=False)

# Database setup
DATABASE_URL = 'sqlite:///purchases.db'  # Example using SQLite
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
