from datetime import datetime
from pydantic import BaseModel
from typing import List

# DTO: Data Transfer Object or Schema
# Represents the structure of the data (data type) as input or output of our API.

class Bouquet_POST_Body (BaseModel):
    bouquetName: str
    bouquetDescription: str
    bouquetComposition: List[str]
    bouquetPrincipal_color: List[str]
    bouquetPrice: float

class Bouquet_PATCH_Body (BaseModel):
    newFeatured: bool

class Bouquet_GETID_Response(BaseModel): # format de sortie (response)TY
    id: int
    name: str
    price: str
    description: str
    principal_color: List[str]
    composition: List[str]
    featured: bool

    class Config: 
        orm_mode= True
        # When returning responses, we often use data from our database.
        # The `orm_mode` configuration allows us to choose which columns to include in the response.

class Customer_POST_Body (BaseModel):
    customerEmail:str
    customerPassword: str
    customerRole: bool

class Customer_PATCH_Body (BaseModel):
    customerRole: bool

class Customer_response (BaseModel): 
    id: int
    email:str
    create_at: datetime
    isAdmin: bool
    # We do not include the password when sending the response.

    class Config: # Important for the ORM to DTO translation.
        orm_mode= True      