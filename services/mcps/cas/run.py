from fastmcp import FastMCP
from dotenv import load_dotenv
import os
from .utils.auth_provider import jwt_verifier
from .auth.server import mcp as auth_mcp
from .user.server import mcp as user_mcp
from .products.server import mcp as products_mcp
from .wishlist.server import mcp as wishlist_mcp
from .cart.server import mcp as cart_mcp
from .userjourney.server import mcp as user_journey_mcp

load_dotenv()

mcp = FastMCP(
    "Conversational Assistant Service MCP",
    auth=jwt_verifier,
    debug=True,
)

mcp.mount("/auth", auth_mcp)
mcp.mount("/user", user_mcp)
mcp.mount("/products", products_mcp)
mcp.mount("/wishlist", wishlist_mcp)
mcp.mount("/cart", cart_mcp)
mcp.mount("/userjourney", user_journey_mcp)

if __name__ == "__main__":
    mcp.run(transport="http", port=int(os.getenv("DEFAULT_PORT")), show_banner=True)
