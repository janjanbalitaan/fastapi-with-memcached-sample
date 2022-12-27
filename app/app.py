from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json


from app.utilities.settings import Settings
from app.utilities.memcached import Memcached
from app.data.data import Data

# routers
from app.api.generic import generic
from app.api.products import products_router

settings = Settings()
memcached = Memcached()
data = Data()

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version
)

# TODO: update this for security purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event("startup")
async def startup():
    # initialize cache data here
    await memcached.set(
        key=f'{settings.memcached_prefix}:all-products',
        value=json.dumps(data.get('products')).encode('utf-8'),
    )
    pass


@app.on_event("shutdown")
async def shutdown():
    await memcached.flushdb()

# routes
app.include_router(generic, prefix='/api/generic', tags=["generic"])
app.include_router(products_router, prefix='/api/products', tags=["products"])