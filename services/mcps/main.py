from fastmcp import FastMCP
from cas.run import mcp as cas_mcp

mcp = FastMCP()
mcp.mount("cas", cas_mcp)

if __name__ == "__main__":
    mcp.run()
