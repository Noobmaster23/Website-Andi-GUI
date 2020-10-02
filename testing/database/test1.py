import psycopg2

conn = psycopg2.connect(host="heebphotography.ch", port="5500", database="dvdrental", user="postgres", password="Y1qhk9nzfI2B")

cur = conn.cursor()

cur.execute("SELECT * FROM film")

records = cur.fetchone()

print(records)