# database/database.py
import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(database="habit_tracker", 
                        user="your_username", 
                        password="your_password",
                        host="your_host", 
                        port="your_port")

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table to store habits
cursor.execute("CREATE TABLE IF NOT EXISTS habits ("
               "id SERIAL PRIMARY KEY,"
               "name TEXT,"
               "date DATE"
               ")")

# Commit the changes and close the connection
conn.commit()
conn.close()
