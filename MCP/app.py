from fastmcp import FastMCP
from Models.jsonResponce import JSONRPCResponse

app = FastMCP("Restaurant DB MCP Server", instructions="An MCP that provides tools for statistical data from a restaurant",)

@app.tool(
	name="get schema",
	description="returns the databases schema",
)
async def get_schema() -> str:
	x = JSONRPCResponse()
	x.set_result("some data to show user")
	return ""

@app.tool()
async def create_row() -> list[str]:
	return [""]

@app.tool()
async def delete_row() -> list[str]:
	return [""]
s
@app.tool()
async def edit_row() -> list[str]:
	return [""]

@app.tool()
async def read_row() -> list[str]:
	return [""]

@app.tool()
async def read_where() -> list[list[str]]:
	return [[""]]

@app.tool()
async def execute_sql() -> list[list[str]]:
	return [[""]]

@app.tool()
async def get_curr_time() -> str:
	return ""
