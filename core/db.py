import sqlite3


class DataBase:
	def __init__(self, db: str):
		self.db: str = db
		self.__conn, self.__cur = self.__connect()
		
	def list_tables(self) -> list:
		self.__cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
		tables: list = self.__cur.fetchall()
		tables = [table[0] for table in tables]
		return tables

	def __connect(self):
		conn: sqlite3.Connection = sqlite3.connect(self.db)
		cur: sqlite3.Cursor = conn.cursor()
		return conn, cur 

	def insert(self, Table, values: tuple) -> None:
		_insert_query: str = f"""INSERT INTO {Table} VALUES {values}"""
		self.__cur.execute(_insert_query)
		self.__conn.commit()

	def fetch(self, table, fields="*", filter_obj=None, filter_val=None, filter_mode="strict") -> list:
		if filter_obj and filter_val:
			if filter_mode=="Strict":
				self.__cur.execute(f"SELECT {fields} FROM {table} WHERE {filter_obj}='{filter_val}'")
			else:
				self.__cur.execute(f"SELECT {fields} FROM {table} WHERE {filter_obj} LIkE '%{filter_val}%'")
		else:
			self.__cur.execute(f"SELECT {fields} FROM {table}")
		results = self.__cur.fetchall()
		return results

	def create_table(self, Table: str, columns: dict) -> None:
		clm: list = []
		for column, dtype in columns.items():
			clm.append(f"{column} {dtype}")
		query: str = f"""CREATE TABLE IF NOT EXISTS {Table} {tuple(clm)}"""
		self.__cur.execute(query)
		self.__conn.commit()

	def delete(self, Table: str, clm_name: str, identifier:str) -> None:
		self.__cur.execute(f"DELETE FROM {Table} WHERE {clm_name}={identifier}")
		self.__conn.commit()

	def update(self, Table: str, clm: str, identifier: str, **kwargs) -> None:
		content: str = ""
		i: int = 0
		for key, val in kwargs.items():
			i+=1
			if len(kwargs.keys()) == i:
				content = content+f"{key}='{val}'"
			else:
				content = content+f"{key}='{val}', "
		sql: str = f"UPDATE {Table} SET {content} WHERE {clm}='{identifier}'"
		self.__cur.execute(sql)
		self.__conn.commit()

