import os
from fastmcp import FastMCP, Context, tools
from pydantic import Field
from ..utils.httpx_utils import fetch_and_parse
from typing import Annotated, Optional
from ..schemas.product import ProductSearchResponse
from dataclasses import dataclass
from fastmcp.server.dependencies import get_access_token, AccessToken


@dataclass
class ProductFilters:
    categories: str = ""
    product_name: str = ""


class ProductsTools:
    def __init__(self):
        # Do any necessary initialization here
        pass

    def register(self, mcp: FastMCP):

        @mcp.tool(
            name="get_all_categories",
            description="Get all categories",
            tags={"products"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def get_all_categories():
            categories = await fetch_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/products/categories",
                model=list[str],
                validate_model=False,
            )
            return categories

        @mcp.tool(
            name="get_products",
            description="Get all products with the matching filter criteria",
            tags={"products"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def get_products(
            ctx: Context,
            category: Annotated[
                Optional[str], Field(description="The category of the product")
            ] = None,
            product_name: Annotated[
                Optional[str], Field(description="The name of the product")
            ] = None,
        ):
            """
            Fetches all products.

            Args:
            category (Optional[str]): The category of the product.
            product_name (Optional[str]): The name of the product.

            Returns:
            Product Model if creation is successful, None otherwise.
            """
            access_token: AccessToken = get_access_token()
            if (category is None or category == "") and (
                product_name is None or product_name == ""
            ):
                result = await ctx.elicit(
                    message="Please provide a category or product name",
                    response_type=ProductFilters,
                )
                if result.action == "accept":
                    category = result.data.categories
                    product_name = result.data.product_name
            # Prepare params
            params = {}
            if product_name is not None and product_name != "":
                params["q"] = product_name
            if category is not None and category != "":
                params["category"] = category

            # If only product name is provided any time do a search else if a catergory is supplied or not do products
            if product_name is None or product_name == "":
                return await fetch_and_parse(
                    url=f"{os.getenv('CAS_API_URL')}/products/",
                    model=ProductSearchResponse,
                    params=params,
                    headers={"Authorization": f"Bearer {access_token.token}"},
                )
            return await fetch_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/products/search",
                model=ProductSearchResponse,
                params=params,
                headers={"Authorization": f"Bearer {access_token.token}"},
            )
