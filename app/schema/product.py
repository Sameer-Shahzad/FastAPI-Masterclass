
from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID


from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

class Product(BaseModel):
    id: UUID
    name: str
    # name: str = "Sameer"  # we can also give default value to the field like name: str = "Default Product Name"
    sku: Annotated [
        str,
        Field(
            description="Stock Keeping Unit - unique identifier for the product",
            example="SKU12345",
            min_length=5,
            max_length=20
        )]
    