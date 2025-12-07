## Initialize the Project

Inside mcps folder open the terminal and ensure uv is installed
```bash
uv venv .venv
.venv\Scripts\activate
uv add -r requirements.txt
uv sync
```

## Command to Debug any Module

```bash
py -m debugpy --listen 5678 --wait-for-client -m  cas.auth.server
```

### MCP Inspector
```bash
npx @modelcontextprotocol/inspector
```

## To Run Main Module
```bash
py -m cas.run
```

## To Run Individual Module
```bash
py -m cas.auth.server
```




