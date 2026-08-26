import mcp
from fastmcp import FastMCP
from Models.jsonRequest import *

TOOLS = [
	{
        "name": "get_schema",
        "description": "get the database's schema",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
	{
        "name": "create_row",
        "description": "create a row in one of the database's tables",
        "parameters": {
            "type": "object",
            "properties": {
                "table": {"type": "string", "description": "the table to insert into"},
                "values": {"type": "array", "description": "the values that get inserted into the table", "items": {
                    "type": "string"
                }}
            },
            "required": ["table", "values"]
        }
    },
	{
        "name": "read_row",
        "description": "read a row in a table",
        "parameters": {
            "type": "object",
            "properties": {
                "table": {"type": "string", "description": "the table to read from"},
                "where": {"type": "string", "description": "the where clause at the end of an sql statement"}
            },
            "required": ["table", "where"]
        }
    },
]

app = FastMCP("Restaurant DB MCP Server", instructions="A database containing statistics about a restaurant",)

@app.tool()
async def get_schema() -> str:
    return ""
