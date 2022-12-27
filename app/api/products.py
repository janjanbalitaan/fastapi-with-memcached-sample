from typing import List, Optional
from fastapi import APIRouter, HTTPException
from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer
import json

from app.data.data import Data
from app.utilities.settings import Settings
from app.utilities.memcached import Memcached
from app.types.products import Product, UpdateProduct
from app.types.responses import HTTPError, HTTPSuccess

products_router = APIRouter()
data = Data()
settings = Settings()
memcached = Memcached()
memcached_key = f'{settings.memcached_prefix}:all-products'

@products_router.get(
    '',
    response_model=List[Product],
)
async def get(
    id: Optional[int] = None,
    title: Optional[str] = None,
):
    query_id = True if id else False
    query_title = True if title else False
    ldata = []
    # use memcached value if the cache was already set
    memcached_value = await memcached.get_dict(
        memcached_key
    )
    
    print(f'will be getting on memcached={memcached_value is not None}')
    rows = memcached_value if memcached_value else data.get("products")
    if not id and not title:
        ldata = rows
    else:
        for row in rows:
            if query_id and query_title:
                if row["id"] == id and row["title"] == title:
                    ldata.append(row)
            else:
                if query_id and row["id"] == id:
                    ldata.append(row)

                if query_title and row["title"] == title:
                    ldata.append(row)

    return ldata

@products_router.post(
    '',
    status_code=201,
    responses={
        201: {
            "model": Product,
            "description": "successfully created a product",
        },
        400: {
            "model": HTTPError,
            "description": "error while creating a product",
        },
    }
)    
async def create(
    payload: Product
):
    try:
        rows = data.get("products")
        for row in rows:
            if row["id"] == payload.id:
                raise Exception(f'id={payload.id} already exists')
        
        is_success, message = data.append(
            "products",
            payload.dict()
        )

        if not is_success:
            raise Exception(message)

        # append also in memcached cache if the key are already set
        memcached_value = await memcached.get_dict(
            memcached_key
        )
        if memcached_value:
            memcached_value.append(
                payload.dict()
            )

            # set the new value for the memcached key
            await memcached.set(
                memcached_key,
                value=json.dumps(memcached_value),
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')
    
    return payload

@products_router.put(
    '/{id}',
    status_code=200,
    responses={
        200: {
            "model": HTTPSuccess,
            "description": "successfully updated a product",
        },
        400: {
            "model": HTTPError,
            "description": "error while updating a product",
        },
    }
)    
async def update(
    id: int,
    payload: UpdateProduct,
):
    try:
        found = False
        rows = data.get("products")
        for idx, row in enumerate(rows):
            if row["id"] == id:
                rows[idx] = {
                    **payload.dict(),
                    "id": id,
                }
                found = True
        if not found:
            raise Exception(f'{id=} does not exist')
        
        is_success, message = data.create(
            "products",
            rows
        )

        if not is_success:
            raise Exception(message)

        # update in memcached cache if the key are already set
        memcached_value = await memcached.get_dict(
            memcached_key
        )
        if memcached_value:
            # set the new value for the memcached key
            await memcached.set(
                memcached_key,
                value=json.dumps(rows),
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')

    return {
        "detail": f'successfully updated {id=}'
    }

@products_router.delete(
    '/{id}',
    status_code=200,
    responses={
        200: {
            "model": HTTPSuccess,
            "description": "successfully deleted a product",
        },
        400: {
            "model": HTTPError,
            "description": "error while deleting a product",
        },
    }
)    
async def delete(
    id: int
):
    try:
        found = False
        rows = data.get("products")
        for idx, row in enumerate(rows):
            if row["id"] == id:
                rows.pop(idx)
                found = True
        if not found:
            raise Exception(f'{id=} does not exist')
        
        is_success, message = data.create(
            "products",
            rows
        )

        if not is_success:
            raise Exception(message)

        # delete in memcached cache if the key are already set
        memcached_value = await memcached.get_dict(
            memcached_key
        )
        if memcached_value:
            # set the new value for the memcached key
            await memcached.set(
                memcached_key,
                value=json.dumps(rows),
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')

    return {
        "detail": f'successfully deleted {id=}'
    }
