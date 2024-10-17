from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, select
from sqlalchemy.orm import sessionmaker, declarative_base,Session  
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn
import datetime

app = FastAPI()
load_dotenv()

# Database setup

# Construct the DATABASE_URL using the environment variables
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

print(DATABASE_URL)  # print the constructed database URL, remove later 

try: 
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    print("Database connection established successfully.")

except Exception as e:
    print(f"Error creating database engine: {e}")

# Define the User model
try:
    class User(Base):
        __tablename__ = 'users'
        user_id = Column(Integer, primary_key=True, index=True)
        email = Column(String, unique=True, index=True)
        phone_number = Column(String, index=True)
        created_at = Column(DateTime)
        updated_at = Column(DateTime)

    print("User model created successfully.")

except Exception as e:
    print(f"Error defining User model: {e}")

# Define the Cryptocurrency model
try:
    class Cryptocurrency(Base):
        __tablename__ = 'cryptocurrencies'
        crypto_id = Column(Integer, primary_key=True, index=True)
        name = Column(String(100), nullable=False)
        market_cap = Column(Float, nullable=True)
        hourly_price = Column(Float, nullable=True)
        hourly_percentage = Column(Float, nullable=True)
        time_updated = Column(DateTime, nullable=True)
        

    print("Cryptocurrency model created successfully.")

except Exception as e:
    print(f"Error defining Cryptocurrency model: {e}")

# Define the Alert model
try:
    class Alert(Base):
        __tablename__ = 'alerts'
        alert_id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
        crypto_id = Column(Integer, ForeignKey('cryptocurrencies.crypto_id'), nullable=False)
        threshold_price = Column(Float)
        threshold_percentage = Column(Float)
        method = Column(String)
        notification_method = Column(String)
        created_at = Column(DateTime)
        updated_at = Column(DateTime)

    print("Alert model created successfully.")

except Exception as e:
    print(f"Error defining Alert model: {e}")

# Define the Notification model
try:
    class Notification(Base):
        __tablename__ = 'notifications'
        notification_id = Column(Integer, primary_key=True, index=True)
        alert_id = Column(Integer, ForeignKey('alerts.alert_id'), nullable=False)
        message = Column(String)
        notification_method = Column(String)
        sent_at = Column(DateTime)

    print("Notification model created successfully.")

except Exception as e:
    print(f"Error defining Notification model: {e}")

# Create the FastAPI app
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

''''''  
@app.get("/cryptocurrencies/", response_model=list)
def get_all_cryptocurrencies(db: Session = Depends(get_db)):
    try:
        # Query the database for all cryptocurrencies
        stmt = select(Cryptocurrency)
        cryptos = db.execute(stmt).scalars().all()

        # If there are no records, return an empty list
        if cryptos:
            return [
                {
                    "id": crypto.crypto_id,
                    "name": crypto.name,
                    "market_cap": crypto.market_cap,
                    "hourly_price": crypto.hourly_price,
                    "time_updated": crypto.time_updated.isoformat() if crypto.time_updated else None,
                    "hourly_percentage": crypto.hourly_percentage,
                }
                for crypto in cryptos
            ]
        else:
            return []  # Return an empty list if no cryptocurrencies are found

    except Exception as e:
        print(f"Error retrieving cryptocurrencies: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
       
''''''        
@app.get("/cryptocurrencies/{crypto_id}", response_model=dict)
def get_cryptocurrency(crypto_id: int, db: Session = Depends(get_db)):
    try:
        # Query the database for the cryptocurrency
        stmt = select(Cryptocurrency).where(Cryptocurrency.crypto_id == crypto_id)
        crypto = db.execute(stmt).scalars().first()
        
        if crypto:
            return {
                "id": crypto.crypto_id,
                "name": crypto.crypto_name,
                "market_cap": crypto.market_cap,
                "hourly_price": crypto.hourly_price,
                "time_updated": crypto.time_updated.isoformat() if crypto.time_updated else None,
                "hourly_percentage": crypto.hourly_percentage,
            }
        else:
            raise HTTPException(status_code=404, detail="Cryptocurrency not found")
    
    except Exception as e:
        # Log the error or print it
        print(f"Error retrieving cryptocurrency: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/cryptocurrencies/", response_model=dict)
def create_cryptocurrency(crypto: dict, db: Session = Depends(get_db)):
    try:
        new_crypto = Cryptocurrency(
            name=crypto['name'],
            market_cap=crypto['market_cap'],
            hourly_price=crypto['hourly_price'],
            hourly_percentage=crypto['hourly_percentage'],
            time_updated=datetime.datetime.now()
        )
        
        db.add(new_crypto)
        db.commit()
        db.refresh(new_crypto)

        return {
            "id": new_crypto.crypto_id,
            "name": new_crypto.name,
            "market_cap": new_crypto.market_cap,
            "hourly_price": new_crypto.hourly_price,
            "hourly_percentage": new_crypto.hourly_percentage,
            "time_updated": new_crypto.time_updated.isoformat()
        }
    
    except Exception as e:
        print(f"Error creating cryptocurrency: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
