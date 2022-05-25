import psycopg2			#for connecting to DB
from psycopg2 import sql

class postgres:
	def runQuery(query, values=[]):
		database = "pokemon"
		user = "postgres"
		password = "pokemonbot"

		try:
			conn=psycopg2.connect("dbname="+database+" user="+user+" password="+password)
		except:
			print("DB connection unsuccessful.")
			exit(0)

		cur = conn.cursor();
		
		cur.execute(sql.SQL(query),[i for i in values]);
		return cur.fetchall()