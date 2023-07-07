from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata

# Database 
from classes.database import database_engine 
import classes.models_orm # Import des ORM

#Import des routers
import routers.router_products, routers.router_customers, routers.router_transactions, routers.router_auth

# Créer les tables si elles ne sont pas présente dans la DB.
classes.models_orm.Base.metadata.create_all(bind=database_engine)

JardinDeden = FastAPI(
    title="Flowers API",
    description=api_description,
    openapi_tags=tags_metadata # tagsmetadat est defnit au dessus
) 

# Ajouter les routers dédiés
JardinDeden.include_router(routers.router_products.router)
JardinDeden.include_router(routers.router_customers.router)
JardinDeden.include_router(routers.router_transactions.router)
JardinDeden.include_router(routers.router_auth.router)

# /*
# #API metadat
# import psycopg2
# from psycopg2.extras import RealDictCursor

# # Connexion DB
# connexion = psycopg2.connect(
#     host="dpg-ciimtjdgkuvojjbv1s40-a.frankfurt-postgres.render.com",
#     database="jardindedendb",
#     user="jardindedendb_user",
#     password="JrFSfPObNaBpXw0TTln7DZILqmGH8MGr",
#     cursor_factory=RealDictCursor
# )
# cursor= connexion.cursor()    

# @JardinDeden.get("/")
# async def root():
#     return {"message": "Hello"}

# flowersList= [
#             {"flowersName": "Rose", "flowersPrice": 50.3},
#             {"flowersName": "Tulipe", "flowersPrice": 18.99}, 
#             {"flowersName": "Oeillet", "flowersPrice": 61.65} 
#         ]

# @JardinDeden.get("/GetFlowers", tags=["Flowers"])
# async def getFlowers():
#     # Requete SQL
#     cursor.execute("SELECT * FROM flower")
#     dbFlowers= cursor.fetchall()
#     return {
#         "Flowers": dbFlowers,
#         "Stock": 10,   
#         "total": 2,
#         "skip": 0  
#     }
    
# #Data models /schema /DTO
# class Flower (BaseModel):
#     flowerName: str
#     flowerPrice: float
#     availability: bool = True # default / optionel
#     rating: Optional[int] # Complement optionnel

# @JardinDeden.post("/PostFlowers", tags=["Flowers"])
# async def PostFlowers(payload: Flower, response:Response):
#     print(payload.flowerName)
#     cursor.execute("INSERT INTO flower (name, price) VALUES (%s,%s) RETURNING *;", (payload.flowerName, payload.flowerPrice))
#     connexion.commit() # Save in the DB (Comme F6 dans PGAdmin)
#     response.status_code = status.HTTP_201_CREATED
#     return {"message": f"New arrivage of flowers in the shop: { payload.flowerName }"}

# @JardinDeden.get('/GetFlowers/{flowers_id}')
# async def get_flowers(flowers_id:int, response:Response):
#     try : 
#         cursor.execute(f"SELECT * FROM flower WHERE id={flowers_id}")
#         corresponding_flowers = cursor.fetchone()
#         if (corresponding_flowers):
#             return corresponding_flowers
#         else:
#             raise HTTPException(
#                 status.HTTP_404_NOT_FOUND,
#                 detail="Flower not found"
#             )
#     except : 
#         raise HTTPException(
#             status.HTTP_404_NOT_FOUND,
#             detail="Flowers not found"
#         )

# @JardinDeden.delete("/flowers/{flowers_id}", tags=["Flowers"])
# async def delete_flowers(flowers_id: int): 
#     cursor.execute(
#         "DELETE FROM flower WHERE id=%s RETURNING *;",
#         (flowers_id,) # don't touch this code, it work and I don't know why
#     )
#     connexion.commit()
#     return {"message":f"Watch deleted updated"} 

# #PUT (ajouter mais sur exister -> remplacer)

# @JardinDeden.put("/flowers/{flowers_id}", tags=["Flowers"])
# async def replace_flowers(flowers_id: int, payload: Flower):
#     cursor.execute(
#         'UPDATE flower SET name=%s, price=%s WHERE id=%s RETURNING *;',
#         (payload.flowerName, payload.flowerPrice,flowers_id)
#     )
#     # test= cursor.fetchone()
#     # print(test)
#     connexion.commit()

#     return {"message":f"Flowers sucessfully updated: {payload.flowerName}"} 
# */*