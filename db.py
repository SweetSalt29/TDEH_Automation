from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'clinic.db')
ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=ENGINE)
Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=False)  # +91XXXXXXXXXX
    patients_age = Column(Integer)
    gender = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    visits = relationship("Visit", back_populates="patient")

class Visit(Base):
    __tablename__ = "visits"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    visit_date = Column(DateTime, default=datetime.utcnow)
    diagnosis = Column(Text)
    meds = Column(Text)
    revisit_date = Column(Date)
    uploaded_file = Column(String)
    patient = relationship("Patient", back_populates="visits")

def init_db():
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    init_db()
    print("Database initialized at", DB_PATH)
