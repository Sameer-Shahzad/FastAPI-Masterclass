from fastapi import FastAPI, HTTPException, Path, Query, Body
# from fastapi.middleware.cors import CORSMiddleware  # This is used to allow cross-origin requests from different domains, which is common in web applications where the frontend and backend are hosted separately.
from app.services.products import get_all_products, add_product, delete, change_product
from pydantic import BaseModel, Field
from app.schema.product import Product
from app.database import engine
from app import models 



models.Base.metadata.create_all(bind=engine) # This line is used to create the tables in the database based on the models defined in the models.py file. It uses the metadata from the Base class to create the tables in the database. The bind=engine argument tells SQLAlchemy which database engine to use for creating the tables.     

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware configuration to allow requests from different origins. This is important for frontend applications that may be hosted on a different domain than the backend API.
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins, you can specify specific origins if needed
#     allow_methods=["*"],  # Allow all HTTP methods, but try to specify only the methods you need for better security
#     allow_headers=["*"],  # Allow all headers
# )   

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def get_items(item_id: int):
    items = ["iPhone", "iPad", "MacBook"]
    return items[item_id]


# @app.get("/products")
# def get_products():
#     return get_all_products()
  

@app.get("/products")
def get_products(category: str = Query(default=None, min_length=1, max_length=50, description="Filter products by category"), offset: int = Query(default=0, ge=0, description="Number of items to skip"), limit: int = Query(default=2, ge=1, le=100, description="Maximum number of items to return")): 
        
    products = get_all_products()
    if category:
        needle = category.strip().lower()
        products = [p for p in products if p.get("category", "").strip().lower() == needle]
        if not products:
            raise HTTPException(status_code=404, detail=f"No products found in category '{category}'")
    total = len(products)    
    products = products[offset:offset+limit]
    return {"total": total, "products": products, "offset": offset, "limit": limit}
            
        
@app.get("/products/{product_id}")
def get_product_by_id(product_id:str = Path(..., description="The ID of the product to retrieve", min_length=36, max_length=36, examples=["123e4567-e89b-12d3-a456-426614174000"])):
    products = get_all_products()
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail=f"Product with id '{product_id}' not found")



# class Product(BaseModel):
#     id: str
#     name: str
#     # name: str = "Sameer" # we can also give default value to the field like name: str = "Default Product Name"
#     sku: Annotated [
#         str,
#         Field(
#             description="Stock Keeping Unit - unique identifier for the product",
#             example="SKU12345",
#             min_length=5,
#             max_length=20
#         )]
    
# @app.post("/products", status_code=201)
# def create_product(product: Product):
#     return product



@app.post("/products", status_code=201) 
def create_product(product: Product = Body(..., description="The product data to create")): # This Product word telling that my data should be in the format of Product class which is defined in product.py file and we are importing that class here in main.py file
    try:
        new_product = product.model_dump(mode="json") 
        
        adding_product = add_product(new_product)
        return adding_product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.delete('/products/{product_id}')
def remove_product(product_id: str = Path(..., description="The ID of the product to delete", min_length=36, max_length=36, examples=["123e4567-e89b-12d3-a456-426614174000"])):
    try:
        message = delete(product_id)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@app.put('/products/{product_id}')
def update_product(
    product_id: str = Path(..., min_length=36, max_length=36), 
    updated_product: Product = Body(...)
):
  try:
        product_dict = updated_product.model_dump(mode="json")    
        
        message = change_product(product_id, product_dict)
        return {"message": message}
        
  except ValueError as e:
    raise HTTPException(status_code=404, detail=str(e))