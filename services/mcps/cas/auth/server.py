from fastmcp import FastMCP
from .tools import AuthTools
from ..utils.auth_provider import remoteAuthProvider
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP(
    "cas_auth_mcp",
    auth=remoteAuthProvider,
    debug=True,
)

auth_tools = AuthTools()
auth_tools.register(mcp=mcp)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=int(os.getenv("DEFAULT_PORT")), show_banner=True)
