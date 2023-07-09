from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from classes import models_orm, schemas_dto, database
import utilities

router = APIRouter(
    prefix='/customers',
    tags=['Customers']
)

# Create a new customer
@router.post('', response_model=schemas_dto.Customer_response, status_code= status.HTTP_201_CREATED)
async def create_customer(
    payload: schemas_dto.Customer_POST_Body, 
    cursor: Session = Depends(database.get_cursor),
    ):
    try: 
        # 1. Hash the password instead of storing it in plain text
        hashed_password = utilities.hash_password(payload.customerPassword)
        # 2. Create an ORM object to be inserted into the database
        new_customer = models_orm.Customers(password=hashed_password, email=payload.customerEmail, isAdmin=payload.customerStatus)
        # 3. Add the new customer to the session
        cursor.add(new_customer)
        # 4. Save the staged changes
        cursor.commit()
        # Refresh the customer object to obtain its ID
        cursor.refresh(new_customer)
        return new_customer
    except IntegrityError: # Triggered if a user with the same email already exists (unique=True)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    
# Retrieve a list of customers
@router.get('')
async def get_all_customers(cursor: Session = Depends(database.get_cursor)):
    all_customers = cursor.query(models_orm.Customers).all()
    return all_customers

# Retrieve a customer by ID
@router.get('/{customer_id}', response_model=schemas_dto.Customer_response)
async def get_user_by_id(customer_id:int, cursor: Session = Depends(database.get_cursor)):
    corresponding_customer = cursor.query(models_orm.Customers).filter(models_orm.Customers.id == customer_id).first()
    if(corresponding_customer):
        return corresponding_customer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No user with id:{customer_id}'
        )