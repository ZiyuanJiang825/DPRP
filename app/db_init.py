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
cur.execute('DROP TABLE IF EXISTS product2reviews;')
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('DROP TABLE IF EXISTS reviews;')
cur.execute('DROP TABLE IF EXISTS products;')
cur.execute('DROP TABLE IF EXISTS review_histories;')
cur.execute('''
    CREATE TABLE users (id serial PRIMARY KEY,
                        username varchar (50) NOT NULL,
                        email varchar (50) NOT NULL,
                        password BYTEA NOT NULL,
                        private_key BYTEA NOT NULL)
            '''
            )
cur.execute('''
        create table reviews
(
	review_id serial primary key,
	user_id int not null,
	tx_hash varchar(500) not null,
	title varchar(50) not null,
	product_name varchar(50) not null,
	review varchar(500) not null,
	pros varchar(200) not null,
	cons varchar(200) not null,
	rating int not null,
	create_time varchar(50) not null
);
''')

cur.execute('''
        create table products
(
	product_id serial primary key,
	product_name varchar(50) not null,
	link varchar(100) not null,
	description varchar(500) not null
);
''')

cur.execute('''
        INSERT INTO products
        VALUES (DEFAULT, 'ipad', 'www.ipad.com','it is an ipad')
''')

cur.execute('''
        create table product2reviews
(
	product_id int,
	review_id int,
	PRIMARY KEY(product_id, review_id),
    CONSTRAINT fk_product
        FOREIGN KEY(product_id)
        REFERENCES products(product_id),
    CONSTRAINT fk_reviews
        FOREIGN KEY(review_id)
        REFERENCES reviews(review_id)
);
''')

cur.execute('''
        create table review_histories
(
    tx_hash varchar(500) primary key,
    review_id int,
    create_time varchar(50)
);
''')

conn.commit()
cur.close()
conn.close()