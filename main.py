from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata

# Database 
from classes.database import database_engine 
import classes.models_orm # Import des ORM

#Import des routers
import routers.router_bouquets, routers.router_customers, routers.router_transactions, routers.router_auth

# Créer les tables si elles ne sont pas présente dans la DB.
classes.models_orm.Base.metadata.create_all(bind=database_engine)

JardinDeden = FastAPI(
    title="Flowers API",
    description=api_description,
    openapi_tags=tags_metadata # tagsmetadat est defnit au dessus
) 

# Ajouter les routers dédiés
JardinDeden.include_router(routers.router_customers.router)
JardinDeden.include_router(routers.router_transactions.router)
JardinDeden.include_router(routers.router_auth.router)
JardinDeden.include_router(routers.router_bouquets.router)
