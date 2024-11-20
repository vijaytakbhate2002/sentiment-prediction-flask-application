import mysql.connector
from mysql.connector import errorcode
import logging
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Handles database connection and operations."""
    
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connects to the database and initializes the cursor."""
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            logging.info("Database connection successful...")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.warning("Invalid username or password for database connection.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.warning("Database does not exist.")
            else:
                logging.error(err)
        finally:
            if self.connection and self.connection.is_connected():
                logging.info("Database is ready for interaction.")
        return self.connection

    def create_table(self, table_name: str = 'USER_INTERACTION') -> None:
        """Creates a table with the specified name."""
        if self.cursor:
            try:
                query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    ID INT PRIMARY KEY AUTO_INCREMENT,
                    user_input VARCHAR(1000),
                    model_output VARCHAR(100),
                    user_satisfaction_level INT DEFAULT NULL,
                    user_suggestion VARCHAR(500)
                )
                """
                self.cursor.execute(query)
                self.connection.commit()
                logging.info(f"Table '{table_name}' created successfully.")
            except mysql.connector.Error as e:
                logging.error(f"Failed to create table: {e}")
        else:
            logging.error("Cursor not initialized. Connect to the database first.")

    def get_cursor(self):
        """Returns the active cursor or raises an error."""
        if self.cursor:
            return self.cursor
        else:
            raise ValueError("Cursor is not initialized. Ensure database connection is established.")



