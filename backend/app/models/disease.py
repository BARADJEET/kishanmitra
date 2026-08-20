from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class DiseasePest(Base):
    __tablename__ = "diseases_pests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    scientific_name = Column(String(255), nullable=True)
    target_crops = Column(String(500), nullable=False)  # Comma separated e.g. "Tomato, Potato, Chilli"
    symptoms = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    prevention_methods = Column(Text, nullable=False)
    severity_level = Column(String(50), default="Medium")  # Low, Medium, High, Critical
    image_sample_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    solutions = relationship("DiseaseSolution", back_populates="disease", cascade="all, delete-orphan")

class DiseaseSolution(Base):
    __tablename__ = "disease_solutions"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases_pests.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_name = Column(String(100), nullable=False)
    recommended_action = Column(Text, nullable=False)
    organic_treatment = Column(Text, nullable=True)
    chemical_treatment = Column(Text, nullable=True)
    safety_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    disease = relationship("DiseasePest", back_populates="solutions")
    products = relationship("Product", back_populates="solution")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    solution_id = Column(Integer, ForeignKey("disease_solutions.id", ondelete="SET NULL"), nullable=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False)  # Fertilizer, Pesticide, Fungicide, Insecticide, Bio-Pesticide, Growth-Promoter
    manufacturer = Column(String(255), nullable=True)
    active_ingredient = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    dosage_instructions = Column(Text, nullable=False)
    suitable_crops = Column(String(500), nullable=True)
    price_estimate = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    solution = relationship("DiseaseSolution", back_populates="products")

class MLPrediction(Base):
    __tablename__ = "ml_predictions"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="SET NULL"), nullable=True)
    image_url = Column(String(500), nullable=False)
    crop_name = Column(String(100), nullable=True)
    predicted_disease = Column(String(255), nullable=False)
    confidence_score = Column(Float, nullable=False)  # 0 to 100
    symptoms = Column(Text, nullable=True)
    recommended_solution = Column(Text, nullable=True)
    prevention = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    farmer = relationship("User", back_populates="ml_predictions")
