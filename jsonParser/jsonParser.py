#=== Imported Modules ===#
import json
import mysql.connector
import re
from table import Table

#=== jsonParser class ===#
class jsonParser:
	def __init__(self, db, datapath, key):
		self.datapath = datapath
		self.jsonObj = {}
		self.key = key
		self.db = db
		self.tables = []


		# get data from file
		try:
			with open(self.datapath, "r") as file:
				whole_json = json.load(file)
				self.jsonObj = whole_json.get(key)
		except FileNotFoundError:
			return

	def parse_to_db(self):
		self.execute_sql(
			f"CREATE TABLE IF NOT EXISTS {self.key} ()"
		)

	def create_db(self, start_json=None, parent=None):
		# get data
		whole_json = start_json
		if whole_json is None:
			try:
				with open(self.datapath, "r") as file:
					whole_json = json.load(file)
			except FileNotFoundError:
				return {}

		new_table = Table()
		new_table.add_column("Id", None, "INTEGER", False)
		for k, v in whole_json.items():
			if type(v) is list:
				if type(v[0]) is dict:
					child_table = Table()
					child_table.add_name(k)
					child_table.copy_columns(self.create_db(whole_json.get(k)[0], child_table))

					if parent is not None:
						child_table.add_column(parent.name+"_Id", parent, "INTEGER", False)

					self.tables.append(child_table.to_sql())
				else:
					pass
			elif type(v) is str:
				new_table.add_column(k, None, "VARCHAR(50)", True)
			elif type(v) is int:
				new_table.add_column(k, None, "INTEGER", True)
			elif type(v) is bool:
				new_table.add_column(k, None, "BOOLEAN", True)
			elif type(v) is float:
				new_table.add_column(k, None, "DECIMAL(5, 2)", True)

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
	statsDB = jsonParser("statsDb", "data/data.json", "shifts")
	statsDB.create_db().to_sql()
	for i in statsDB.tables:
		print(i)
