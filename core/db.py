import sqlite3


class DataBase:
	def __init__(self, db):
		self.db = db
		self.__conn, self.__cur = self.__connect()

	def __exit__(self, exc_type, exc_value, traceback):
		self.conn.close()

	def __connect(self):
		conn = sqlite3.connect(self.db)
		cur = conn.cursor()
		return conn, cur 

	def insert(self, Table, values: tuple):
		_insert_query = f"""INSERT INTO {Table} VALUES {values}"""
		self.__cur.execute(_insert_query)
		self.__conn.commit()

	def fetch(self, table, fields="*", filter_obj=None, filter_val=None, filter_mode="strict"):
		if filter_obj and filter_val:
			if filter_mode=="Strict":
				self.__cur.execute(f"SELECT {fields} FROM {table} WHERE {filter_obj}='{filter_val}'")
			else:
				self.__cur.execute(f"SELECT {fields} FROM {table} WHERE {filter_obj} LIkE '%{filter_val}%'")
		else:
			self.__cur.execute(f"SELECT {fields} FROM {table}")
		results = self.__cur.fetchall()
		return results
