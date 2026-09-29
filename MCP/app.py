import os
from datetime import datetime
from fastmcp import FastMCP
import datetime
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
db_name = os.getenv('DATABASE', 'statsDb')
app = FastMCP(
	"Restaurant DB MCP Server",
	instructions="An MCP server that connects to a mySQL database. When referencing a table name or a column name, you must use backticks (`) to denote them."
)

@app.tool(
	name="get-tables",
	description="returns a list of all the database's tables"
)
async def get_tables() -> list[dict[str, str | list]]:
	conn = mysql.connector.connect(
		host="mysql",
		port=3306,
		user="root",
		password="root",
		database=db_name
	)
	cursor = conn.cursor()
	cursor.execute("SHOW TABLES;")

	results = cursor.fetchall()
	# Convert tuples to lists and handle different data types
	response = []
	for row in results:
		for item in row:
			try:
				response.append({"table_name": str(item)})
			except Exception:
				continue

	for table in response:
		cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table['table_name']}';")
		results = cursor.fetchall()
		table["columns"] = []
		for row in results:
			for item in row:
				try:
					table["columns"].append(item)
				except Exception:
					continue

	cursor.close()
	conn.close()
	return response

@app.tool(
	name="read",
	description="for executing SELECT sql")
async def read(sql: str) -> list[list[str]]:
	if not "SELECT" in sql:
		return [["you must use a SELECT statement; for INSERT, UPDATE, and DELETE use execute_sql(sql: str)"]]
	if "DROP" in sql or "RENAME" in sql or "ALTER" in sql:
		return [["insufficient permissions"]]

	conn = mysql.connector.connect(
		host="mysql",
		port=3306,
		user="root",
		password="root",
		database=db_name
	)
	cursor = conn.cursor()
	cursor.execute(sql)

	results = cursor.fetchall()
	# Convert tuples to lists and handle different data types
	response = []
	for row in results:
		response.append([])
		for item in row:
			try:
				response[-1].append(item)
			except Exception:
				continue
	cursor.close()
	conn.close()

	return response

@app.tool(
	name="execute-sql",
	description="for executing INSERT, UPDATE, and DELETE sql"
)
async def execute_sql(sql: str) -> str:
	if "DROP" in sql or "RENAME" in sql or "ALTER" in sql:
		return "insufficient permissions"

	try:
		conn = mysql.connector.connect(
			host="mysql",
			port=3306,
			user="root",
			password="root",
			database=db_name
		)
		cursor = conn.cursor()

		cursor.execute(sql)
		conn.commit()
		cursor.close()
		conn.close()

		return "success"

	except Exception as ex:
		return f"failed to execute sql: {ex}"

@app.tool(
	name="get-timestamp",
	description="returns the current datetime"
)
async def get_curr_time() -> str:
	return str(datetime.datetime.now())

@app.tool(
	name="rename-table",
	description="renames a table in the database"
)
async def rename_table(old_name: str, new_name: str) -> str:
	try:
		conn = mysql.connector.connect(
			host="mysql",
			port=3306,
			user="root",
			password="root",
			database=db_name
		)
		cursor = conn.cursor()

		cursor.execute(f"RENAME TABLE {old_name} TO {new_name};")
		conn.commit()
		cursor.close()
		conn.close()

		return "success"
	except Exception as ex:
		return f"failed to execute sql: {ex}"

@app.tool(
	name="rename-column",
	description="renames a column of a table"
)
async def rename_column(table: str, old_name: str, new_name: str) -> str:
	try:
		conn = mysql.connector.connect(
			host="mysql",
			port=3306,
			user="root",
			password="root",
			database=db_name
		)
		cursor = conn.cursor()

		cursor.execute(f"ALTER TABLE {table} RENAME COLUMN {old_name} TO {new_name};")
		conn.commit()
		cursor.close()
		conn.close()

		return "success"
	except Exception as ex:
		return f"failed to execute sql: {ex}"

if __name__ == "__main__":
	app.run(transport="http", host="0.0.0.0", port=8000)
