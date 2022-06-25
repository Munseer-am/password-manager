import config
import sqlite3

def txt_log(app, time, script):
	with open(f"{config.log_dir}/logs.log", "a") as f:
		f.write(
			f"\nTime: {time} Script: {script} Application: {app.capitalize()}")
		f.close()

def log(app, time, script):
	log_con = sqlite3.connect(config.database_file_path)
	cur = self.log_con.cursor()
	insertQuery = f"""INSERT INTO LOG VALUES (?, ?, ?)"""
	cur.execute(insertQuery, (app.capitalize(), time, script))
	log_con.commit()
	log_con.close()
