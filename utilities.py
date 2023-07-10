from passlib.context import CryptContext
from jose import jwt, JWTError
from classes.database import get_cursor
from classes import models_orm, schemas_dto
from jose import jwt, JWTError
# Import OAuth2PasswordBearer for authentication
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth')  # OAuth2PasswordBearer for token authentication
pwd_context = CryptContext(schemes=["bcrypt"])  # Password hashing context

# Hash a password using bcrypt
def hash_password(clear_password: str):
    return pwd_context.hash(clear_password)

# Verify a password against a hashed password using bcrypt
def verify_password(given_password, hashed_password):
    return pwd_context.verify(given_password, hashed_password)

# JWT authentication
algo = 'HS256'  # Algorithm for JWT
secret = '5ae48e781d227cabc077167f64005ff949922d586157d6ae07078fee3f3ad170'  # Secret key for JWT

# Generate a JWT token for authentication
def generate_token(given_id: int):
    payload = {"customer_id": given_id}
    encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
    print(encoded_jwt)
    return {
        "access_token": encoded_jwt,  # JWT
        "token_type": "bearer"
    }

# Decode and retrieve the customer ID from the JWT token
def decode_token(given_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(given_token, secret, algorithms=algo)
        decoded_id = payload.get('customer_id')
    except JWTError:  # if JWT is not provided or has an invalid signature
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return decoded_id

def get_customer_by_id(customer_id: int):
    customer = models_orm.Customers.query.filter(models_orm.Customers.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer not found with ID: {customer_id}"
        )
    return customer

def check_role (payload:int = Depends(decode_token)):
    customer_id = payload
    customer =  get_customer_by_id(customer_id)
    if customer.isAdmin != "true" :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JUST for admin"
        )
    else:
        return payload