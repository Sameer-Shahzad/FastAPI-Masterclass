import json
from pathlib import Path
from typing import List, Dict


# DATA_FILE = Path("..", "data", "products.json")
DATA_FILE = Path(__file__).parent.parent / "data" / "products.json" 

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_all_products() -> List[Dict]:
    return load_products()


def save_product(product:List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(product, f, indent=4, ensure_ascii=False)
        
        
def add_product(product:Dict) -> None:
    products = load_products()
    if products and any(p["id"] == product["id"] for p in products):
        raise ValueError(f"Product with id '{product['id']}' already exists")
    products.append(product)
    save_product(products)
    return product