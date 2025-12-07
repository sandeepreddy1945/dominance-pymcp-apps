from fastmcp import FastMCP
from .tools import AuthTools
from ..utils.auth_provider import verifier, jwt_verifier
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP(
    "cas_auth_mcp",
    auth=jwt_verifier,
    debug=True,
)

auth_tools = AuthTools()
auth_tools.register(mcp=mcp)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=int(os.getenv("DEFAULT_PORT")), show_banner=True)
