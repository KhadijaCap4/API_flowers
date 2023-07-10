from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm, schemas_dto
import utilities
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/bouquets',
    tags=['Bouquets']
)

# Retrieve a list of bouquets
@router.get('')
async def get_bouquets(
    cursor: Session= Depends(get_cursor), 
    limit:int=10, offset:int=0):
    all_bouquets = cursor.query(models_orm.Bouquets).limit(limit).offset(offset).all() # Lancement de la requête
    bouquets_count= cursor.query(func.count(models_orm.Bouquets.id)).scalar()
    return {
        "bouquets": all_bouquets,
        "limit": limit,
        "total": bouquets_count,
        "skip":offset
    }

# Retrieve a bouquet by ID
@router.get('/{bouquet_id}', response_model=schemas_dto.Bouquet_GETID_Response)
async def get_bouquet(bouquet_id:int, cursor:Session= Depends(get_cursor)):
    corresponding_bouquet = cursor.query(models_orm.Bouquets).filter(models_orm.Bouquets.id == bouquet_id).first()
    if(corresponding_bouquet):  
        return corresponding_bouquet
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding bouquet found with id : {bouquet_id}"
        )

# Create a new bouquet
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_bouquet(payload: schemas_dto.Bouquet_POST_Body, cursor:Session= Depends(get_cursor)):
    new_bouquet = models_orm.Bouquets(name=payload.bouquetName, description=payload.bouquetDescription, composition=payload.bouquetComposition, principal_color=payload.bouquetPrincipal_color, price=payload.bouquetPrice) # build the insert
    cursor.add(new_bouquet) # Send the query
    cursor.commit() #Save the staged change
    cursor.refresh(new_bouquet)
    return {"message" : f"New bouquet {new_bouquet.name} added sucessfully with id: {new_bouquet.id}"} 


# Delete a bouquet if you are authenticated and an admin 
@router.delete('/{bouquet_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletes_bouquet(bouquet_id: int, token: str = Depends(oauth2_scheme),  cursor: Session = Depends(get_cursor)):
    decoded_customer_id = utilities.decode_token(token)
    corresponding_bouquet = cursor.query(models_orm.Bouquets).filter(models_orm.Bouquets.id == bouquet_id).first()
    corresponding_customer = cursor.query(models_orm.Customers).filter(models_orm.Customers.id == decoded_customer_id).first()
    if corresponding_customer.isAdmin == True :
        if corresponding_bouquet:
            # Supprimer toutes les transactions associées au bouquet
            cursor.query(models_orm.Transactions).filter(models_orm.Transactions.bouquet_id == bouquet_id).delete()
            # Supprimer le bouquet lui-même
            cursor.delete(corresponding_bouquet)
            cursor.commit()
            return
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No corresponding bouquet with id: {bouquet_id}"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not an Admin"
        )
    
# Update a bouquet
@router.patch('/{bouquet_id}')
async def update_bouquet(bouquet_id: int, payload:schemas_dto.Bouquet_PATCH_Body, cursor:Session=Depends(get_cursor)):
    # trouver le bouquet correspodant
    corresponding_bouquet = cursor.query(models_orm.Bouquets).filter(models_orm.Bouquets.id == bouquet_id)
    if(corresponding_bouquet.first()):
        # mise à jour (quoi avec quelle valeur ?) Body -> DTO
        corresponding_bouquet.update({'featured':payload.newFeatured})
        cursor.commit()
        return corresponding_bouquet.first()
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ne corresponding bouquet with id: {bouquet_id}'
        )