from fastmcp import FastMCP, Context, tools
from pydantic import Field
from ..schemas.order import OrderResponse
from ..utils.httpx_utils import post_and_parse, fetch_and_parse, put_and_parse
from typing import Annotated, Optional
import os
from fastmcp.server.dependencies import get_access_token, AccessToken
from dataclasses import dataclass


class OrderTools:
    def __init__(self):
        pass

    def register(self, mcp: FastMCP):

        @mcp.tool(
            name="orders_checkout",
            description="Checkout the order",
            tags={"orders"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def orders_checkout(ctx: Context):
            """
            Checkout the order
            """
            access_token: AccessToken = get_access_token()
            ctx.report_progress(progress=0.5, message="Checking out the order", total=1)
            order = await post_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/orders/checkout",
                model=OrderResponse,
                headers={"Authorization": f"Bearer {access_token.token}"},
                payload={},
            )
            ctx.report_progress(progress=1, message="Order checked out", total=1)
            return order

        @mcp.tool(
            name="orders_history",
            description="Get the order history",
            tags={"orders"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def orders_history(ctx: Context):
            """
            Get the order history
            """
            access_token: AccessToken = get_access_token()
            ctx.report_progress(progress=0.5, message="Fetching order history", total=1)
            orders = await fetch_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/orders/history",
                model=list[OrderResponse],
                headers={"Authorization": f"Bearer {access_token.token}"},
            )
            ctx.report_progress(progress=1, message="Order history fetched", total=1)
            return orders
