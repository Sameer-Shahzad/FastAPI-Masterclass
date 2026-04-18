from fastapi import FastAPI, HTTPException, Path, Query
from app.services.products import get_all_products

app = FastAPI()

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
def get_product_by_id(product_id:str = Path(..., description="The ID of the product to retrieve", min_length=36, max_length=36, des="The ID of the product to retrieve", example="123e4567-e89b-12d3-a456-426614174000")):
    products = get_all_products()
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail=f"Product with id '{product_id}' not found")