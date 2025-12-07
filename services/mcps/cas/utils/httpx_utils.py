import httpx
from typing import Optional, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


async def fetch_and_parse(
    url: str,
    model: Type[T],
    headers: Optional[dict[str, str]] = {},
    params: Optional[dict[str, str]] = {},
    validate_model: bool = True,
) -> T:
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return model.model_validate(data) if validate_model else data


async def post_and_parse(
    url: str,
    model: Type[T],
    payload: Optional[dict] = None,
    headers: Optional[dict[str, str]] = {},
    params: Optional[dict[str, str]] = {},
    validate_model: bool = True,
) -> T:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return model.model_validate(data) if validate_model else data


async def put_and_parse(
    url: str,
    model: Type[T],
    payload: Optional[dict] = None,
    headers: Optional[dict[str, str]] = {},
    params: Optional[dict[str, str]] = {},
    validate_model: bool = True,
) -> T:
    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=payload, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return model.model_validate(data) if validate_model else data


async def delete_and_parse(
    url: str,
    model: Type[T],
    headers: Optional[dict[str, str]] = {},
    params: Optional[dict[str, str]] = {},
    validate_model: bool = False,
) -> T:
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return model.model_validate(data) if validate_model else data
