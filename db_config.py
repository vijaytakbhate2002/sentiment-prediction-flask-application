import mysql.connector
from mysql.connector import errorcode
import logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define the log format
    handlers=[
        logging.FileHandler('app.log'),  # Log to a file named app.log
        logging.StreamHandler()  # Also log to console
    ]
)

# Database connection details
db_config = {
    'host': '35.232.7.238',
    'user': 'root',
    'password': 'root',
    'database': 'user_activities'
}

try:  
  
    connection = mysql.connector.connect(  
        user=db_config['user'],  
        password=db_config['password'],  
        host=db_config['host'], 
        database=db_config['database'], 
        auth_plugin='mysql_native_password'
    )  
    print("Connection successful!")  

    # Example query (optional)  
    cursor = connection.cursor()  
    cursor.execute("SHOW DATABASES;")  
    for db in cursor:  
        print(db)  

except mysql.connector.Error as err:  
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:  
        print("Something is wrong with your user name or password")  
    elif err.errno == errorcode.ER_BAD_DB_ERROR:  
        print("Database does not exist")  
    else:  
        print(err)  
finally:  
    if 'connection' in locals() and connection.is_connected():  
        connection.close()  
        print("Connection closed.")

