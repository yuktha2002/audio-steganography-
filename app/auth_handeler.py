from jose import JWTError, jwt
from datetime import datetime, timedelta

from app import schemas, models, get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = 'asdhfjfvajsdkvflksadfblke4564jkrhasbfgt47iagi74'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20


def create_access_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expiry})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exeption):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exeption
        token_data = schemas.tokenData(id=id)
    except JWTError:
        raise credentials_exeption
    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='Could not validate the creditainals',
                                         headers={'WWW-Authenticate': 'Bearer'})

    token = verify_access_token(token, credentials_exeption)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
