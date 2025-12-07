# MCP generated using the Open API Contract from the conversational assistant service.

from fastmcp import FastMCP
import httpx
import yaml

client = httpx.AsyncClient(
    base_url="http://localhost:8000",
    headers={"Content-Type": "application/json", "Accept": "application/json"},
)

openapi_spec_url = "http://localhost:8000/openapi.json"
openapi_spec = httpx.get(openapi_spec_url).json()

# openapi_spec = yaml.safe_load( open("openapi.yaml", "r"))

mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="conversational_assistant_mcp",
    version="1.0.0",
)

if __name__ == "__main__":
    mcp.run(transport="http", port=9000, show_banner=True)
