from fastmcp import FastMCP
from .tools import OrderTools
from ..utils.auth_provider import jwt_verifier
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP(
    "cas_order_mcp",
    auth=jwt_verifier,
    debug=True,
)

order_tools = OrderTools()
order_tools.register(mcp=mcp)

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        port=int(os.getenv("DEFAULT_PORT")),
        show_banner=True,
    )
