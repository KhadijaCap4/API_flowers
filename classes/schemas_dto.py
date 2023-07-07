from datetime import datetime
from pydantic import BaseModel
from typing import List

# DTO : Data Transfert Object ou Schema
# Représente la structure de la données (data type) en entrée ou en sortie de notre API.

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
    class Config: # Lors des réponses, nous avons souvant à utiliser les données sortie de notre database. La Config ORM nous permet de "choisir" les columnes à montrer. 
        orm_mode= True

class Customer_POST_Body (BaseModel):
    customerEmail:str
    customerPassword: str

class Customer_response (BaseModel): 
    id: int
    email:str
    create_at: datetime
    # not sending the password
    class Config: # Importante pour la traduction ORM -> DTO
        orm_mode= True      