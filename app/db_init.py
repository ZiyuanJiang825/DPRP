import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="dprp",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('''
    CREATE TABLE users (id serial PRIMARY KEY,
                        username varchar (50) NOT NULL,
                        email varchar (50) NOT NULL,
                        password varchar (50) NOT NULL,
                        private_key varchar (100) NOT NULL)
            '''
            )
conn.commit()
cur.close()
conn.close()