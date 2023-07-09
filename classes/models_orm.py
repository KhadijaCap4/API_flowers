from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Numeric, ARRAY
from sqlalchemy.ext.declarative import declarative_base

# Base class for creating models
Base= declarative_base()

# ORM classes are Python classes based on database tables

class Bouquets(Base):
    __tablename__= "bouquet"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    composition = Column(ARRAY(String), nullable=False)
    principal_color = Column(ARRAY(String), nullable=False)
    price = Column(Numeric, nullable=False)
    featured = Column(Boolean, nullable=True, server_default='FALSE') # server_default sets a default value
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')  # now() represents the current date/time

class Customers(Base):
    __tablename__="customer"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')  
    isAdmin = Column(Boolean, nullable=False, server_default='FALSE')

class Transactions(Base):
    __tablename__="transaction"
    id= Column(Integer, primary_key=True, nullable=False)
    customer_id= Column(Integer, ForeignKey("customer.id", ondelete="RESTRICT"), nullable=False)  # Foreign Keys are based on the primary keys of other tables, but it's not mandatory
    bouquet_id = Column(Integer, ForeignKey("bouquet.id", ondelete="RESTRICT"), nullable=False) # ondelete defines the cascade action when deleting (e.g., delete a transaction, should it delete the customer or the bouquet?)
    transaction_date=Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")