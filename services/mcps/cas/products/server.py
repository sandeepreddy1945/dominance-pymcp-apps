from fastmcp import FastMCP
from .tools import ProductsTools
from ..utils.auth_provider import remoteAuthProvider
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP(
    "cas_products_mcp",
    auth=remoteAuthProvider,
    debug=True,
)

products_tools = ProductsTools()
products_tools.register(mcp=mcp)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=int(os.getenv("DEFAULT_PORT")), show_banner=True)
