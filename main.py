from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata

# Database
from classes.database import database_engine
import classes.models_orm  # Import ORM models

# Import routers
import routers.router_bouquets
import routers.router_customers
import routers.router_transactions
import routers.router_auth

# Create database tables if they don't exist
classes.models_orm.Base.metadata.create_all(bind=database_engine)

JardinDeden = FastAPI(
    title="Flowers API",
    description=api_description,
    openapi_tags=tags_metadata  # tags_metadata is defined above
)

# Add dedicated routers
JardinDeden.include_router(routers.router_customers.router)
JardinDeden.include_router(routers.router_transactions.router)
JardinDeden.include_router(routers.router_auth.router)
JardinDeden.include_router(routers.router_bouquets.router)
