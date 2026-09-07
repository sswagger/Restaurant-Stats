class Table:
	def __init__(self):
		self.name = ""

		# {
		#     "key": "x",
		#     "table": Table,
		#     "type": "INTEGER",
		#     "nullable": False
		# }
		self.columns: list[dict[str, str | bool | None]] = []

	def to_sql(self):
		return [self.name, self.columns]

	def add_column(self, key, table, col_type, nullable):
		self.columns.append({"key": key, "table": table, "type": col_type, "nullable": nullable})

	def copy_columns(self, table):
		for i in table.columns:
			self.add_column(i["key"], i["table"], i["type"], i["nullable"])

	def add_name(self, name):
		self.name = name
