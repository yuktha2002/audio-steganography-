from fastapi import FastAPI
from app import Base, engine
from app.routes import encrypt_router, users_router, auth_router

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get('/ping')
def ping():
    return {'message': 'Hello'}


app.include_router(encrypt_router)
app.include_router(users_router)
app.include_router(auth_router)
