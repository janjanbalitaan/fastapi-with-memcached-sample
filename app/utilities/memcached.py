from typing import Any, Optional
import aiomcache
import json

from app.utilities.settings import Settings

class Memcached:
    
    settings = Settings()
    keys = [
        f'{settings.memcached_prefix}:all-products',
        # TODO: add above all the keys that will be used for the project
    ]
    
    def connect(
        self
    ):
        memcached = aiomcache.Client(
            host=self.settings.memcached_host,
            port=self.settings.memcached_port,
        )

        return memcached

    async def set(
        self,
        key: str,
        value: Any,
        expiry: Optional[int] = 0
    ):
        connection = self.connect()
        value = await connection.set(
            key=key.encode('utf-8'),
            value=value,
            exptime=expiry
        )
        return value

    async def get(
        self,
        key: str
    ):
        connection = self.connect()
        value = await connection.get(key.encode('utf-8'))
        return value

    async def delete(
        self,
        key: str
    ):
        connection = self.connect()
        value = await connection.delete(key.encode('utf-8'))
        return value

    async def get_dict(
        self,
        key: str
    ):
        value = await self.get(key)
        return json.loads(value) if value else None

    async def flushdb(
        self,
    ):
        for key in self.keys:
            await self.delete(key)