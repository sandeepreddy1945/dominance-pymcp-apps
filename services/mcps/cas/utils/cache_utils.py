import redis
from typing import Optional, TypeVar, Type
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class RedisClient:
    _instance: Optional["RedisClient"] = None
    _client: Optional[redis.Redis] = None

    def __init__(self):
        if self._client is None:
            self._pool = redis.ConnectionPool.from_url(
                url="redis://localhost:6379/0",
                decode_responses=True,  # Helps avoid bytes handling
                max_connections=10,
            )
            self._client = redis.Redis(connection_pool=self._pool)

    def __new__(cls, *args, **kwargs):
        # Ensures only ONE instance is created (Singleton)
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
        return cls._instance

    @property
    def get(self, key: str) -> dict:
        return self._client.get(key)

    @property
    def set(self, key: str, value: str):
        self._client.set(key, value)

    @property
    def setex(self, key: str, value: str, ex: int):
        self._client.setex(key, value, ex)

    @property
    def client(self) -> redis.Redis:
        """Returns the Redis client instance"""
        return self._client

    @property
    def set_model(self, key: str, value: T, ex: int = 60):
        self._client.set(key, value.json(), ex=ex)

    @property
    def get_model(self, key: str, model: Type[T]) -> T:
        value = self._client.get(key)
        return model.parse_raw(value)


redis_client = RedisClient().client
