import psycopg2

connection = None

try:
    connection = psycopg2.connect(
        dbname="application_ffr_db",
        user="dev",
        password="ballon",
        host="127.0.0.1",
        port="5432"
    )
    print("Connection successful")
except psycopg2.DatabaseError as e:
    print("Database connection error:", repr(e))
except Exception as e:
    print("An error occurred:", repr(e))
finally:
    if connection is not None:
        connection.close()
        print("Connection closed")
