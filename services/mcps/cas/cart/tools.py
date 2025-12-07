from ..schemas.cart import CartItemResponse, CartResponse
from fastmcp import FastMCP, Context, tools
from pydantic import Field
from ..utils.httpx_utils import post_and_parse, fetch_and_parse, delete_and_parse
from typing import Annotated, Optional
import os
from fastmcp.server.dependencies import get_access_token, AccessToken
from dataclasses import dataclass


class CartTools:
    def __init__(self):
        pass

    def register(self, mcp: FastMCP):
        @mcp.tool(
            name="add_to_cart",
            description="Add a product to the cart",
            tags={"cart"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def add_to_cart(
            ctx: Context,
            product_id: Annotated[str, Field(description="Product ID")],
            quantity: Annotated[int, Field(description="Quantity")],
        ):
            """Adds a product to the cart"""
            access_token: AccessToken = get_access_token()
            response = await post_and_parse(
                url=os.getenv("API_URL") + "/cart/add",
                headers={"Authorization": f"Bearer {access_token}"},
                payload={"product_id": product_id, "quantity": quantity},
                model=CartItemResponse,
            )
            return response

        @mcp.tool(
            name="clear_cart",
            description="Clear the cart",
            tags={"cart"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def clear_cart(ctx: Context):
            """Clears the cart"""
            access_token: AccessToken = get_access_token()
            response = await delete_and_parse(
                url=os.getenv("API_URL") + "/cart/clear",
                headers={"Authorization": f"Bearer {access_token}"},
                model=str,
            )
            return response

        @mcp.tool(
            name="get_cart",
            description="Get the cart",
            tags={"cart"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def get_cart(ctx: Context):
            """Gets the cart"""
            access_token: AccessToken = get_access_token()
            response = await fetch_and_parse(
                url=os.getenv("API_URL") + "/cart/",
                headers={"Authorization": f"Bearer {access_token}"},
                model=CartResponse,
            )
            return response

        @mcp.tool(
            name="cart_summary",
            description="Get the cart summary",
            tags={"cart"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def cart_summary(ctx: Context):
            """Gets the cart summary"""
            access_token: AccessToken = get_access_token()
            response = await fetch_and_parse(
                url=os.getenv("API_URL") + "/cart/summary",
                headers={"Authorization": f"Bearer {access_token}"},
                model=dict,
                validate_model=False,
            )
            return response
