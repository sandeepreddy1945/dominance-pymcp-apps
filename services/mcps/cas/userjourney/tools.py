from fastmcp import FastMCP, Context, tools
from pydantic import Field
from ..utils.httpx_utils import post_and_parse
from typing import Annotated, Optional
import os
from fastmcp.server.dependencies import get_access_token, AccessToken


class UserJourneyTools:
    def __init__(self):
        pass

    def register(self, mcp: FastMCP):

        @mcp.tool(
            name="completePurchaseJourney",
            description="Completes the purchase journey for a product.",
            tags={"userjourney"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def complete_purchase_journey(
            ctx: Context,
            product_id: Annotated[str, Field(description="Product ID")] = None,
        ):
            """
            Completes the purchase journey for a product.
            """
            access_token: AccessToken = get_access_token()
            ctx.report_progress(
                progress=0.5, message="Completing purchase journey", total=1
            )
            if product_id is None:
                purchase_journey = await post_and_parse(
                    url=f"{os.getenv('CAS_API_URL')}/journey/purchase",
                    model=dict,
                    headers={"Authorization": f"Bearer {access_token.token}"},
                    payload={"product_id": product_id},
                    validate_model=False,
                )
            else:
                purchase_journey = await post_and_parse(
                    url=f"{os.getenv('CAS_API_URL')}/journey/purchase",
                    model=dict,
                    headers={"Authorization": f"Bearer {access_token.token}"},
                    validate_model=False,
                )
            ctx.report_progress(
                progress=1, message="Purchase journey completed", total=1
            )
            return purchase_journey
