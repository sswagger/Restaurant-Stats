from datetime import datetime
from fastmcp import FastMCP
import datetime

app = FastMCP("Restaurant DB MCP Server", instructions="An MCP that provides tools for statistical data from a restaurant")

@app.tool(
	name="get-schema",
	description="returns the database's schema",
)
async def get_schema() -> str:
	x = "some data to show user"
	return x

@app.tool()
async def create_row() -> str:
	return ""

@app.tool()
async def delete_row() -> list[str]:
	return [""]

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

@app.tool(
	name="get-timestamp",
	description="returns the current datetime"
)
async def get_curr_time() -> str:
	return str(datetime.datetime.now())

if __name__ == "__main__":
	app.run(transport="http", host="0.0.0.0", port=8000)
