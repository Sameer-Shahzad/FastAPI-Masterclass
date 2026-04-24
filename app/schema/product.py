
import re
from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field, field_validator, computed_field, model_validator

app = FastAPI()

# This class is for post request, we are telling FastAPI than after all the conditions are satisfied, the request body should be converted to this class and then we can use it in our endpoint function. This is also called data validation and serialization.
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


@field_validator("sku")
def validate_sku(cls, value: str) -> str:
    if not value.isupper():
        raise ValueError("SKU must be uppercase")
    
    pattern = r"^[0-9A-Z]{8}-[0-9A-Z]{4}-[0-9A-Z]{4}-[0-9A-Z]{4}-[0-9A-Z]{8}$"
    if not re.match(pattern, value):
        raise ValueError("SKU must be in the format XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX where X is an uppercase letter or a digit")
    return value


@model_validator(mode="after")
def check_name_and_sku(self) -> Product:
    if self.name.lower() == self.sku.lower():
        raise ValueError("Product name should not be part of the SKU")
    return self
