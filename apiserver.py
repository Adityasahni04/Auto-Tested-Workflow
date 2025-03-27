import logging
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# MySQL Database Configuration
DATABASE_URL = "mysql+mysqlconnector://root:aditya2004@localhost:3306/calculations_db"

# Create Database Engine
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    logger.info("✅ Connected to MySQL database successfully!")
except Exception as e:
    logger.error(f"❌ Failed to connect to MySQL: {e}")

Base = declarative_base()

# Model for storing calculations
class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    operation = Column(String(50), index=True)
    num1 = Column(Integer, nullable=False)
    num2 = Column(Integer, nullable=False)
    result = Column(Integer, nullable=False)

# Create tables in MySQL
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully!")
except Exception as e:
    logger.error(f"❌ Error creating database tables: {e}")

# FastAPI app initialization
app = FastAPI()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI MySQL Calculator"}

# Addition API
@app.get("/add/{num1}/{num2}")
def add(num1: int, num2: int, db: Session = Depends(get_db)):
    result = num1 + num2
    db_entry = Calculation(operation="add", num1=num1, num2=num2, result=result)
    db.add(db_entry)
    db.commit()
    logger.info(f"✔️ Addition performed: {num1} + {num2} = {result}")
    return {"operation": "addition", "result": result}

# Subtraction API
@app.get("/subtract/{num1}/{num2}")
def subtract(num1: int, num2: int, db: Session = Depends(get_db)):
    result = num1 - num2
    db_entry = Calculation(operation="subtract", num1=num1, num2=num2, result=result)
    db.add(db_entry)
    db.commit()
    logger.info(f"✔️ Subtraction performed: {num1} - {num2} = {result}")
    return {"operation": "subtraction", "result": result}

# Multiplication API
@app.get("/multiply/{num1}/{num2}")
def multiply(num1: int, num2: int, db: Session = Depends(get_db)):
    result = num1 * num2
    db_entry = Calculation(operation="multiply", num1=num1, num2=num2, result=result)
    db.add(db_entry)
    db.commit()
    logger.info(f"✔️ Multiplication performed: {num1} * {num2} = {result}")
    return {"operation": "multiplication", "result": result}

# Fetch last 10 calculations
@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    history = db.query(Calculation).order_by(Calculation.id.desc()).limit(10).all()
    logger.info("📜 Fetching last 10 calculations from history")
    return {"history": [{"operation": h.operation, "num1": h.num1, "num2": h.num2, "result": h.result} for h in history]}

# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting FastAPI server...")
    uvicorn.run("apiserver:app", host="0.0.0.0", port=8000, reload=True)
