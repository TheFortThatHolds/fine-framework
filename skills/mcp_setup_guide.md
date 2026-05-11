# F.I.N.E. — MCP Setup Guide

F.I.N.E. does not ship with an MCP server. This guide explains how to wrap it as one so you can call it from Claude Desktop, Cursor, or any MCP-compatible client. Build your own — it's your sovereignty.

## Prerequisites

```bash
pip install mcp fine-framework  # or clone the repo
```

## Minimal MCP server

Create `fine_mcp_server.py` alongside your F.I.N.E. installation:

```python
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import sys
sys.path.insert(0, "/path/to/your/FINE")  # point at your FINE install
from fine import compile_feeling

app = Server("fine")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="compile_feeling",
            description="F.I.N.E. emotional compiler. Pass raw feeling input, get output in the requested format.",
            inputSchema={
                "type": "object",
                "properties": {
                    "input": {"type": "string", "description": "Raw feeling input — any length, any format"},
                    "target": {
                        "type": "string",
                        "enum": ["song", "prose", "protocol", "boundary", "poem"],
                        "default": "song"
                    },
                    "feedback": {"type": "string", "description": "Optional feedback from a previous run"}
                },
                "required": ["input"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "compile_feeling":
        result = compile_feeling(
            arguments["input"],
            arguments.get("target", "song"),
            arguments.get("feedback")
        )
        return [types.TextContent(type="text", text=result)]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

## Claude Desktop config

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "fine": {
      "command": "python",
      "args": ["/path/to/fine_mcp_server.py"],
      "env": {
        "FINE_LLM_URL": "http://127.0.0.1:8080/v1",
        "FINE_MODEL": "gemma4e4b"
      }
    }
  }
}
```

## Notes

- The MCP server runs locally on your machine. Nothing is hosted, nothing is shared.
- Point `FINE_LLM_URL` at whatever LLM you're running — local or cloud API.
- Growth reports still write to your local `reports/growth/` directory.
- `compile_feeling()` is synchronous — the async wrapper above handles the MCP protocol layer.
