from fastmcp import FastMCP, Context, tools
from pydantic import Field
from ..schemas.user import UserResponse, UserUpdate
from ..utils.httpx_utils import post_and_parse, fetch_and_parse, put_and_parse
from typing import Annotated, Optional
import os
from fastmcp.server.dependencies import get_access_token, AccessToken
from dataclasses import dataclass


@dataclass
class UserUpdatePreferences:
    full_name: str = ""
    locale: str = ""
    interests: str = ""
    avatar_url: str = ""


class UserTools:
    def __init__(self):
        pass

    def register(self, mcp: FastMCP):

        @mcp.tool(
            name="whoAmI",
            description="Get the current logged in user details using the token",
            tags={"user"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def whoAmI(ctx: Context):
            """
            Fetches the user details based on the token provided.
            In case the token is not fetched from previous calls then re-autenticate the user.
            """
            access_token: AccessToken = get_access_token()
            ctx.report_progress(progress=0.5, message="Fetching user details", total=1)
            user = await fetch_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/users/me",
                model=UserResponse,
                headers={"Authorization": f"Bearer {access_token.token}"},
            )
            ctx.report_progress(progress=1, message="User details fetched", total=1)
            return user

        @mcp.tool(
            name="updateUserPreferences",
            description="Updates the user preferences based on the token and the parameters provided.",
            tags={"user"},
            meta={"auth_level": "user", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def updateUserPreferences(
            ctx: Context,
            full_name: Annotated[
                Optional[str], Field(description="Full name of the user")
            ] = None,
            locale: Annotated[
                Optional[str], Field(description="Locale of the user")
            ] = None,
            interests: Annotated[
                Optional[list[str]], Field(description="Interests of the user")
            ] = None,
            preferences: Annotated[
                Optional[dict[str, str]], Field(description="Preferences of the user")
            ] = None,
            avatar_url: Annotated[
                Optional[str], Field(description="Avatar URL of the user")
            ] = None,
        ) -> UserUpdate:
            """
            Updates the user preferences based on the token and the parameters provided.
            """
            if (
                full_name is None
                or ""
                and locale is None
                or ""
                and interests is None
                or []
                and preferences is None
                or {}
                and avatar_url is None
                or ""
            ):
                preferences = await ctx.elicit(
                    message="Please provide at least one of the parameters for updating user preferences",
                    response_type=UserUpdatePreferences,
                )

                if preferences.action == "accept":
                    full_name = preferences.data.full_name
                    locale = preferences.data.locale
                    if preferences.data.interests is not None:
                        interests = list(preferences.data.interests.split(","))
                    else:
                        interests = []
                    avatar_url = preferences.data.avatar_url
                else:
                    raise ValueError("User preferences not accepted")

            userUpdatePreferences: UserUpdate = UserUpdate(
                full_name=full_name,
                locale=locale,
                interests=interests,
                avatar_url=avatar_url,
            )
            access_token: AccessToken = get_access_token()
            ctx.report_progress(
                progress=0.5, message="Updating user preferences", total=1
            )
            user = await put_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/users/me",
                model=UserResponse,
                headers={"Authorization": f"Bearer {access_token.token}"},
                payload=userUpdatePreferences.dict(),
            )
            ctx.report_progress(progress=1, message="User preferences updated", total=1)
            return user

        @mcp.tool(
            name="listUsers",
            description="Lists all the users in the system. Works only for admin users.",
            tags={"user"},
            meta={"auth_level": "admin", "version": "1.0.0", "author": "sandeep reddy"},
        )
        async def listUsers(ctx: Context) -> list[UserResponse]:
            """
            Lists all the users in the system. Works only for admin users.
            """
            access_token: AccessToken = get_access_token()
            ctx.report_progress(progress=0.5, message="Listing users", total=1)
            users = await fetch_and_parse(
                url=f"{os.getenv('CAS_API_URL')}/users",
                model=list[UserResponse],
                headers={"Authorization": f"Bearer {access_token.token}"},
            )
            ctx.report_progress(progress=1, message="Users listed", total=1)
            return users
