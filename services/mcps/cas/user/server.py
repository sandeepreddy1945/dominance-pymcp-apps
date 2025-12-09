from fastmcp import FastMCP
from .tools import UserTools
from ..utils.auth_provider import remoteAuthProvider
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP(
    "cas_user_mcp",
    auth=remoteAuthProvider,
    debug=True,
)

user_tools = UserTools()
user_tools.register(mcp=mcp)

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        port=int(os.getenv("DEFAULT_PORT")),
        show_banner=True,
    )
