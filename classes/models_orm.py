from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Numeric, ARRAY
from sqlalchemy.ext.declarative import declarative_base

# Class de base pour créer les models
Base= declarative_base()

# Les ORM sont des classes python basée sur les tables de notre base de données

class Bouquets(Base):
    __tablename__= "bouquet"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    composition = Column(ARRAY(String), nullable=False)
    principal_color = Column(ARRAY(String), nullable=False)
    price = Column(Numeric, nullable=False)
    featured = Column(Boolean, nullable=True, server_default='FALSE') # server_default permet de donner une valeur par default
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')  #now() représente la date/time actuelle

class Customers(Base):
    __tablename__="customer"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')  

class Transactions(Base):
    __tablename__="transaction"
    id= Column(Integer, primary_key=True, nullable=False)
    customer_id= Column(Integer, ForeignKey("customer.id", ondelete="RESTRICT"), nullable=False)  # Les Foreign Keys sont basés sur les clé principales des autres tables mais ce n'est pas obligatoire
    bouquet_id = Column(Integer, ForeignKey("bouquet.id", ondelete="RESTRICT"), nullable=False) # ondelete permet de choisir la cascade d'action suite à la suppression (supprimer une transation, doit-elle suppimer le customer ou le produit?)
    transaction_date=Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")