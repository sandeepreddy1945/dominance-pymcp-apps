import uuid
from fastmcp import FastMCP, Context, tools
from pydantic import Field
from ..utils.httpx_utils import post_and_parse, fetch_and_parse, delete_and_parse
from typing import Annotated, Optional
import os
from fastmcp.server.dependencies import get_access_token, AccessToken
from dataclasses import dataclass
from ..schemas.wishlist import (
    WishlistResponse,
    WishlistItemResponse,
)


class WishlistTools:
    def __init__(self):
        pass

    def register(self, mcp: FastMCP):
        @mcp.tool(
            name="getWishlist",
            description="Get the wishlist of the current logged in user",
            tags={"wishlist"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def getWishlist(ctx: Context) -> WishlistResponse:
            """
            Fetches the wishlist of the current logged in user.
            """
            access_token: AccessToken = get_access_token()
            ctx.report_progress(progress=0.5, message="Fetching wishlist", total=1)
            wishlist = await fetch_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/wishlist/",
                model=WishlistResponse,
                headers={"Authorization": f"Bearer {access_token.token}"},
            )
            ctx.report_progress(progress=1, message="Wishlist fetched", total=1)
            return wishlist

        @mcp.tool(
            name="addItemToWishlist",
            description="Add an item to the wishlist of the current logged in user",
            tags={"wishlist"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def addItemToWishlist(
            ctx: Context,
            product_id: Annotated[str, Field(description="Product ID")],
            notes: Annotated[str, Field(description="Notes")] = None,
        ) -> WishlistItemResponse:
            """
            Adds an item to the wishlist of the current logged in user.
            """
            access_token: AccessToken = get_access_token()
            ctx.report_progress(
                progress=0.5, message="Adding item to wishlist", total=1
            )
            wishlist = await post_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/wishlist/add",
                model=WishlistItemResponse,
                headers={"Authorization": f"Bearer {access_token.token}"},
                payload={"product_id": product_id, "notes": notes},
            )
            ctx.report_progress(progress=1, message="Item added to wishlist", total=1)
            return wishlist

        @mcp.tool(
            name="clearWishlist",
            description="Clear the wishlist of the current logged in user",
            tags={"wishlist"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def clearWishlist(ctx: Context) -> str:
            """
            Clears the wishlist of the current logged in user.
            """
            access_token: AccessToken = get_access_token()
            ctx.report_progress(progress=0.5, message="Clearing wishlist", total=1)
            wishlist_message = await delete_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/wishlist/clear",
                model=str,
                headers={"Authorization": f"Bearer {access_token.token}"},
            )
            ctx.report_progress(progress=1, message="Wishlist cleared", total=1)
            return wishlist_message
