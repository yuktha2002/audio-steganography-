from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import User, verify_password, create_access_token, schemas, get_db
router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)


@router.post('/', response_model=schemas.token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid credentials')

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid credentials')
    access_token = create_access_token(data={'user_id': user.id})
    return {'access_token': access_token, 'token_type': 'Bearer'}
