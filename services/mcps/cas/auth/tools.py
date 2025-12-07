from fastmcp import FastMCP, Context, tools
from pydantic import Field
from ..schemas.user import Token, UserFullResponse
from ..utils.httpx_utils import post_and_parse, fetch_and_parse
from typing import Annotated, Optional
from ..schemas.user import UserCreate
import json
import os
from fastmcp.server.dependencies import get_access_token, AccessToken


class AuthTools:
    def __init__(self):
        # Do any necessary initialization here
        pass

    def register(self, mcp: FastMCP):

        @mcp.tool(
            name="register_user",
            description="Register a new user with username and password and fetch back the user details.",
            tags={"authentication"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def register_user(userPayload: Annotated[UserCreate, Field(description="The user payload")]):
            """
            Registers a new user based on provided username and password.

            Args:
            userPayload (UserCreate): The user payload.

            Returns:
            Token Model if registration is successful, None otherwise.
            """
            user = await post_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/auth/register",
                payload=userPayload,
                model=Token,
            )

            return user

        @mcp.tool(
            name="get_current_user_info",
            description="Get the current logged in user details using the token",
            tags={"authentication"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def get_current_user_info(ctx: Context):
            access_token : AccessToken = get_access_token()
            """
            Fetches the user details based on the token provided.
            In case the token is not fetched from previous calls then re-autenticate the user.
            Args:
            token (str) : The jwt token fetched from the user login action
            """
            # token = ctx.request_context.request.user.access_token.token  
            
            user = await fetch_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/auth/me",
                model=UserFullResponse,
                headers={"Authorization": f"Bearer {access_token.token}"},
            )
            return user

        # @mcp.tool(
        #     name="authenticate_user",
        #     description="Authenticate a user with username and password and fetch back the user details.",
        #     tags={"authentication"},
        #     meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        # )
        # async def authenticate_user(
        #     username: Annotated[str, Field(description="The username of the user.")],
        #     password: Annotated[str, Field(description="The password of the user.")],
        # ) -> Token | None:
        #     """
        #     Authenticates a user based on provided username and password.

        #     Args:
        #     username (str): The username of the user.
        #     password (str): The password of the user.

        #     Returns:
        #     Token Model if authentication is successful, None otherwise.
        #     """
        #     user = await post_and_parse(
        #         url=f"{os.getenv('CA_API_URL')}/auth/login",
        #         payload={"username": username, "password": password},
        #         model=Token,
        #     )

        #     return user

        # @mcp.tool(
        #     name="get_current_user_info",
        #     description="Get the current logged in user details using the token",
        #     tags={"authentication"},
        #     meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        # )
        # async def getCurrentUserInfo(
        #     ctx: Context,
        #     token: Annotated[
        #         Optional[str],
        #         Field(
        #             description="JWT Token fecthed from the user authentication call"
        #         ),
        #     ] = None,
        # ) -> UserFullResponse | None:
        #     """
        #     Fetches the user details based on the token provided.
        #     In case the token is not fetched from previous calls then re-autenticate the user.
        #     Args:
        #     token (str) : The jwt token fetched from the user login action
        #     """

        #     if token is None or token is "":
        #         prompt = f""" Since there user is not authenticated previously ask the user to authenticate first.
        #         Use the tool authenticate_user in order to authenticate him and once the token is obtained use the token and fetch the user details.
        #         After fetching the response extract the token from the payload and respond with token alone back.
        #         """
        #         response = await ctx.sample(prompt)
        #         tool = await mcp.get_tool("get_current_user_info")
        #         response = await tool.run({"token": response.text.strip()})
        #         if response.content:
        #             block = response.content[0]
        #             if block.type == "application/json":
        #                 return UserFullResponse(**block.data)
        #             elif block.type == "text":
        #                 data = json.loads(block.text)
        #                 return UserFullResponse(**data)
        #     else:
        #         user = await fetch_and_parse(
        #             url="http://localhost:8000/api/auth/me",
        #             model=UserFullResponse,
        #             headers={"Authorization": f"Bearer {token}"},
        #         )
        #         return user

        #     return None

        # @mcp.tool(
        #     name="refresh_expired_token",
        #     description="Refresh the expired token",
        #     tags={"authentication"},
        #     meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        # )
        # async def refreshExpiredToken(
        #     ctx: Context,
        #     token: Annotated[
        #         Optional[str],
        #         Field(
        #             description="JWT Token fecthed from the user authentication call"
        #         ),
        #     ] = None,
        # ) -> UserFullResponse | None:
        #     """
        #     Refresh the user token based on the inital token provided.
        #     In case the token is not fetched from previous calls then re-autenticate the user.
        #     Args:
        #     token (str) : The jwt token fetched from the user login action
        #     """
        #     if token is None or token is "":
        #         prompt = f""" Since there user is not authenticated previously ask the user to authenticate first.
        #         Use the tool authenticate_user in order to authenticate him and once the token is obtained use the token and fetch the user details.
        #         After fetching the response extract the token from the payload and respond with token alone back.
        #         """
        #         response = await ctx.sample(prompt)
        #         tool = await mcp.get_tool("get_current_user_info")
        #         response = await tool.run({"token": response.text.strip()})
        #         if response.content:
        #             block = response.content[0]
        #             if block.type == "application/json":
        #                 return UserFullResponse(**block.data)
        #             elif block.type == "text":
        #                 data = json.loads(block.text)
        #                 return UserFullResponse(**data)
        #     else:
        #         user = await post_and_parse(
        #             url="http://localhost:8000/api/auth/refresh",
        #             model=UserFullResponse,
        #             headers={"Authorization": f"Bearer {token}"},
        #             payload=None,
        #         )
        #         return user

        #     pass
