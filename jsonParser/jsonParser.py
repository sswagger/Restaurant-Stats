#=== Imported Modules ===#
import json
import mysql.connector

from app import execute_sql


class jsonParser:
	def __init__(self, db, datapath, key):
		self.datapath = datapath
		self.jsonObj = {}
		self.key = key
		self.db = db


		# get data from file
		try:
			with open(self.datapath, "r") as file:
				whole_json = json.load(file)
				self.jsonObj = whole_json.get(key)
		except FileNotFoundError:
			return

	def parse_to_db(self):
		execute_sql(
			f"CREATE TABLE IF NOT EXISTS {self.key} ()"
		)

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
	print(statsDB.get_json([16, "tips"]))
