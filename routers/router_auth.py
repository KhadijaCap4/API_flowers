from fastapi import APIRouter, HTTPException, status, Depends
from classes import schemas_dto, database, models_orm
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import utilities
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# Create an instance of APIRouter for the /auth endpoint
router = APIRouter(
    prefix='/auth',
    tags=["Auth"]
)

# Endpoint for authenticating a customer
@router.post('', status_code=status.HTTP_201_CREATED)
async def auth_customer(
        payload : OAuth2PasswordRequestForm= Depends(), 
        cursor: Session= Depends(database.get_cursor)
    ):
    print(payload.__dict__)
    # 1. Retrieve credentials (username as it comes from the default FastAPI form)
    corresponding_customer = cursor.query(models_orm.Customers).filter(models_orm.Customers.email == payload.username).first()
    # 2. Check if the user exists in the database
    if(not corresponding_customer):
         raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail='email not good'
         )
    # 3. Verify the hashed password (Bad practice, should return 404 in both cases)
    valid_pwd = utilities.verify_password(
        payload.password,
        corresponding_customer.password
     )
    if(not valid_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='password not good' 
        ) 
    # 4. Generate JWT (JSON Web Token)
    token = utilities.generate_token(corresponding_customer.id)
    print(token)
    return token