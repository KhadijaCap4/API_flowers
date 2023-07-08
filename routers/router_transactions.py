from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm
import utilities
from sqlalchemy.exc import IntegrityError
from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

# Retrieve a list of transactions for the authenticated customer
@router.get('')
async def list_transactions(token: Annotated[str, Depends(oauth2_scheme)], cursor: Session = Depends(get_cursor)):
    # Decoding the token to retrieve the customer ID
    decoded_customer_id = utilities.decode_token(token)
    all_transactions = cursor.query(models_orm.Transactions).filter(models_orm.Transactions.customer_id == decoded_customer_id).all()
    return all_transactions

# DTO for creating a new transaction
class TransactionPost(BaseModel):
    bouquet_id: int

# Create a new transaction for the authenticated customer
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_transaction(token: Annotated[str, Depends(oauth2_scheme)], payload: TransactionPost, cursor: Session = Depends(get_cursor)):
    decoded_customer_id = utilities.decode_token(token)
    new_transaction = models_orm.Transactions(customer_id=decoded_customer_id, bouquet_id=payload.bouquet_id)
    try:
        cursor.add(new_transaction)
        cursor.commit()
        cursor.refresh(new_transaction)
        return {'message': f'New transaction added on {new_transaction.transaction_date} with ID: {new_transaction.id}'}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='The given bouquet does not exist'
        )
