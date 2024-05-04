from app import models, schemas
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from app import get_db, hass_password


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/users_create',
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.userOut)
def user_Create(user: schemas.userCreate,
                db: Session = Depends(get_db)):
    search_user = db.query(models.User).filter(models.User.email == user.email)
    if search_user.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'{user.email} is already created')
    user.password = hass_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/get_user_by_id/{id}',
            response_model=schemas.userOut)
def get_user(id: int,
             db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id).first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'userid with {id} not found')
    return get_user
