from sqlalchemy import Column, String, Float, Integer, Boolean, JSON
from app.database import Base

class ProductModel(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, index=True)
    brand = Column(String)
    
    price = Column(Float, nullable=False)
    discount_percent = Column(Float, default=0.0)
    stock = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=0.0)
    
    tags = Column(JSON, default=[]) 
    image_urls = Column(JSON, default=[])
    dimensions_cm = Column(JSON) 
    seller = Column(JSON) 
    
    created_at = Column(String) 
    
