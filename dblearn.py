# import psycopg2

# hostname = 'localhost'
# database = 'demo'
# username = 'postgres'
# pwd = 'utkarsh123'
# port_id = 5432

# conn  = None
# cur = None
# try:
#     conn = psycopg2.connect(
#         host = hostname,
#         dbname = database,
#         user = username,
#         password = pwd,
#         port = port_id
#     )

#     cur = conn.cursor()
#     # cur.execute('DROP TABLE IF EXISTS employee')

#     create_script = """
#                     CREATE TABLE IF NOT EXISTS employee(
#                     id int PRIMARY KEY,
#                     name varchar(40) NOT NULL,
#                     salary int,
#                     dept_id varchar(20))
#                                             """
#     cur.execute(create_script)

#     insert_script = 'INSERT INTO employee (id, name, salary, dept_id) VALUES (%s,%s,%s,%s)'
#     insert_values = (2,'utkarsh',12000,'D1')
                     
#     # for record in insert_values:

#     cur.execute(insert_script,insert_values)
#     conn.commit()

# except Exception as error:
#     print(error)

# finally:
#     if cur is not None:
#         cur.close() 
#     if conn is not None:
#         conn.close()
       
import psycopg2

hostname = 'localhost'
database = 'demo'
username = 'postgres'
pwd = 'utkarsh123'
port_id = 5432

conn = None
cur = None
try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    print("Connected to the database successfully!")

    cur = conn.cursor()

    # Drop table if exists
    cur.execute('DROP TABLE IF EXISTS employee')

    # Create table
    create_script = """
                    CREATE TABLE IF NOT EXISTS employee(
                    id int PRIMARY KEY,
                    name varchar(40) NOT NULL,
                    salary int,
                    dept_id varchar(20))
                                            """
    cur.execute(create_script)

    # Insert values
    insert_script = 'INSERT INTO employee (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'
    insert_values = [
        (1, 'utkarsh', 12000, 'D1'),
        (2, 'anuj', 15000, 'D2'),
        (3, 'Pratham', 20000, 'D3'),
    ]
    for record in insert_values:
        cur.execute(insert_script, record)

    cur.execute('SELECT * FROM EMPLOYEE')
    for record in cur.fetchall():
        print(record)    

    # Commit the transaction
    conn.commit()
    print("Values inserted successfully!")

except Exception as error:
    print("Error:", error)

finally:
    # Close the cursor and connection
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    print("Database connection closed.")
