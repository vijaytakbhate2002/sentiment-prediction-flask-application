import sys
sys.path.append('\\'.join(__file__.split('\\')[:-2]))
import config
from db_operations.db_connection import DatabaseConnection
import logging
from config import USER, HOST, DATABASE, PASSWORD, PORT

logger = logging.getLogger(__name__)

class DatabaseOperations:
    db_connection = DatabaseConnection(host=HOST, user=USER, database=DATABASE, password=PASSWORD, port=PORT)
    db = db_connection.connect()
    db_connection.create_table()
    cursor = db_connection.get_cursor()
    print("DB connection is successful ...")

    def readLast(self) -> dict:
        """Fetches the last row from the table based on the highest ID and returns it as a formatted dictionary."""
        try:
            query = f"SELECT * FROM {config.DB_NAME} WHERE ID = (SELECT MAX(ID) FROM {config.DB_NAME})"
            self.cursor.execute(query)
            last_row = self.cursor.fetchone()

            if last_row:
                formatted_row = {
                    "ID": last_row[0],
                    "user_input": last_row[1],
                    "model_prediction": last_row[2],
                    "user_satisfaction_level": last_row[3],
                    "user_suggestion": last_row[4],
                }
                logging.info("Last row retrieved successfully.")
                return formatted_row
            else:
                logging.info("Table is empty. No rows to fetch.")
                return None
        except Exception as e:
            logging.error(f"Failed to retrieve the last row: {e}")
            return {"error": "Error occurred while fetching the last row."}

    def insertRow(self, user_input: str, model_prediction: str, user_satisfaction_level: int, user_suggestion: str):
        """Inserts a new row into the database."""
        try:
            query = f"""INSERT INTO {config.DB_NAME} 
                        (`user_input`, `model_output`, `user_satisfaction_level`, `user_suggestion`)
                        VALUES (%s, %s, %s, %s)"""
            values = (user_input, model_prediction, user_satisfaction_level, user_suggestion)
            self.cursor.execute(query, values)
            self.db.commit()
            logging.info(f"Data insertion successful: {values}")
        except Exception as e:
            logging.error(f"Data insertion failed: {e}")

    def deleteLast(self):
        """Deletes the last row based on the highest ID (assuming ID is the primary key)."""
        try:
            query = f"DELETE FROM {config.DB_NAME} WHERE ID = (SELECT MAX(ID) FROM {config.DB_NAME})"
            self.cursor.execute(query)
            self.db.commit()
            logging.info("Last row deleted successfully.")
        except Exception as e:
            logging.error(f"Failed to delete the last row: {e}")

    def replaceLastIfSame(self, user_input: str, model_prediction: str, user_satisfaction_level: int, user_suggestion: str):
        """Replaces the last row in the database if the latest user_input is the same as the last user_input."""
        try:
            last_row = self.readLast()
            if last_row and last_row['user_input'] == user_input:
                self.deleteLast()
            self.insertRow(user_input, model_prediction, user_satisfaction_level, user_suggestion)
        except Exception as e:
            logging.error(f"Failed to replace last row: {e}")

    def findInDB(self, user_input: str) -> str:
        """Finds a given user_input in the database and returns the corresponding model prediction."""
        try:
            query = f"SELECT `model_prediction` FROM {config.DB_NAME} WHERE `user_input` = %s"
            self.cursor.execute(query, (user_input,))
            prediction = self.cursor.fetchone()
            if prediction:
                logging.info(f"Prediction found for user_input: {user_input}")
                return prediction[0]
            else:
                logging.info(f"No prediction found for user_input: {user_input}")
                return None
        except Exception as e:
            logging.error(f"Failed to find prediction: {e}")
            return None
        
    def updateLastRow(self, user_satisfaction_level: str, user_suggestion: str) -> None:
        """Updates the last row by modifying user_satisfaction_level and user_suggestion in the database."""
        try:
            query = f"""
                            UPDATE {config.DB_NAME}
                            SET user_satisfaction_level = %s, user_suggestion = %s
                            WHERE ID = (
                                SELECT max_id FROM (
                                    SELECT MAX(ID) AS max_id FROM {config.DB_NAME}
                                ) AS subquery
                            )
                            """
            values = (user_satisfaction_level, user_suggestion)

            self.cursor.execute(query, values)
            self.db.commit()
            logging.info(f"Last row updated successfully: user_satisfaction_level={user_satisfaction_level}, user_suggestion={user_suggestion}")
        except Exception as e:
            logging.error(f"Failed to update the last row: {e}")
