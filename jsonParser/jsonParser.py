#=== Imported Modules ===#
import json
import time

import mysql.connector
import re
from table import Table

#=== jsonParser class ===#
class jsonParser:
	def __init__(self, db, datapath):
		self.datapath = datapath
		self.jsonObj = {}
		self.db = db
		self.tables = []


		# get data from file
		try:
			with open(self.datapath, "r") as file:
				whole_json = json.load(file)
				self.jsonObj = whole_json
		except FileNotFoundError:
			return

	def parse_to_db(self):
		pass

	def create_db_schema(self, start_json=None, parent=None):
		# get data
		whole_json = start_json
		if whole_json is None:
			whole_json = self.jsonObj

		# create a new table
		new_table = Table()
		found_pk = False
		# loop through json
		for k, v in whole_json.items():
			# look for an id already defined
			if "Id" in k:
				found_pk = True
			curr_table_i = len(self.tables)

			# check the type of the value
			if type(v) is list:
				if type(v[0]) is dict:
					# if it's a list of dictionaries, then it is a child table

					# create a new table, and add the name
					child_table = Table()
					child_table.add_name(k)
					# get the columns from it
					child_table.copy_columns(self.create_db_schema(whole_json.get(k)[0], child_table))

					# add current table's name as parent
					if parent is not None:
						if len(child_table.pk) > 0:
							child_table.add_column(parent.name+"_Id", parent, "INTEGER", True)
							child_table.add_pk(parent.name+"_Id")
						else:
							child_table.add_column(parent.name+"_Id", parent, "INTEGER", False)

						# add it to the list of tables
					self.tables.insert(curr_table_i, child_table)

			elif type(v) is str:
				# if it is a string, then it is either a datetime or a varchar
				pat = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
				if re.search(pat, v):
					new_table.add_column(k, None, "DATETIME", True)
				else:
					new_table.add_column(k, None, "VARCHAR(50)", True)
			elif type(v) is int:
				# if it's an int, then check if it's an id
				if "_Id" in k:
					for j in self.tables:
						if j.name == k[:-3]:
							new_table.add_column(k, j, "INTEGER", True)
							new_table.add_pk(str(k))
							found_pk = True
				else:
					new_table.add_column(k, None, "INTEGER", True)
			elif type(v) is bool:
				# boolean
				new_table.add_column(k, None, "BOOLEAN", True)
			elif type(v) is float:
				# decimal
				new_table.add_column(k, None, "DECIMAL(5, 2)", True)

		if not found_pk :
			new_table.add_column("Id", None, "INTEGER", False)

		return new_table

	def get_json(self, keys:list, i:int=0, start_json=None):
		# get or set json object
		json_obj = start_json
		if json_obj is None:
			json_obj = self.jsonObj

		if i + 1 < len(keys):
			# if we haven't reached the end of keys, get the value and continue
			return self.get_json(keys, i=i+1, start_json=json_obj[keys[i]])
		else:
			# since this is the last key, just return the value
			return json_obj[keys[i]]

	def get_table(self):
		pass

	def execute_sql(self, sql):
		# Connect to MySQL
		conn = mysql.connector.connect(
			host="localhost",
			port=3306,
			user="root",
			password="root",
			database=self.db
		)
		cursor = conn.cursor()

		cursor.execute(sql)
		conn.commit()
		cursor.close()
		conn.close()


if __name__ == "__main__":
	print(r"╔==================================================╗")
	print(r"║             /||   /||||   /||\   ||  ||          ║")
	print(r"║              ||  ||      ||  ||  ||| ||          ║")
	print(r"║              ||   \||\   ||  ||  ||||||          ║")
	print(r"║          ||  ||      ||  ||__||  || |||          ║")
	print(r"║           \||||  ||||/    \||/   ||  ||          ║")
	print(r"║                                                  ║")
	print(r"║   /||\    /||\    /||\    /||||   /||||   /||\   ║")
	print(r"║  ||__||  ||__||  ||__||  ||      ||      ||__||  ║")
	print(r"║  ||||/   ||||||  ||||/    \||\   ||||||  ||||/   ║")
	print(r"║  ||      ||  ||  || \\       ||  ||      || \\   ║")
	print(r"║  ||      ||  ||  ||  \\  ||||/    \||||  ||  \\  ║")
	print(r"╠==================================================╣")
	print(r"║   Ensure data/data.json contains data to parse   ║")
	print(r"╚==================================================╝")

	db = input("What is the name of the database? : ")
	print("reading json from data/data.json...")
	statsDB = jsonParser(db, "data/data.json")
	print("converting to sql...")
	statsDB.create_db_schema().to_sql()

	for i in statsDB.tables:
		print(i.to_sql())

	user_sql = input("Execute SQL? [Y]es|[n]o: ")
	if "y" in user_sql.lower():
		for i in statsDB.tables:
			statsDB.execute_sql(i.to_sql())
			time.sleep(1)

		print("SQL run Successfully!")
