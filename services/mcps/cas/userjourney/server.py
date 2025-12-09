from fastmcp import FastMCP
from .tools import UserJourneyTools
from ..utils.auth_provider import remoteAuthProvider
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP(
    "cas_user_journey_mcp",
    auth=remoteAuthProvider,
    debug=True,
)

user_journey_tools = UserJourneyTools()
user_journey_tools.register(mcp=mcp)

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        port=int(os.getenv("DEFAULT_PORT")),
        show_banner=True,
    )
