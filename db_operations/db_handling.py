import sys
sys.path.append('\\'.join(__file__.split('\\')[:-2]))
import config
from db_operations.db_connection import DatabaseConnection
import logging
from config import USER, HOST, DATABASE, PASSWORD


class DatabaseOperations:
    db = DatabaseConnection(host=HOST,user=USER, database=DATABASE, password=PASSWORD).connect()
    db.create_table()
    cursor = db.get_cursor()

    def readLast(self) -> dict:
        """Fetches the last row from the table based on the highest ID and returns it as a formatted string."""
        try:
            query = f"""SELECT * FROM {config.DB_NAME} 
                        WHERE ID = (SELECT MAX(ID) FROM {config.DB_NAME})"""
            self.cursor.execute(query)
            last_row = self.cursor.fetchone()  

            if last_row:
            
                formatted_row = {"ID": last_row[0], "user_input":last_row[1], 
                                 "model_prediction":last_row[2], "user_satisfaction_level":last_row[3], 
                                 "user_suggestion":last_row[4]}
                
                logging.info("Last row retrieved successfully.")
                return formatted_row
            else:
                logging.info("Table is empty. No rows to fetch.")
                return None
            
        except Exception as e:
            logging.error(f"Failed to retrieve the last row: {e}")
            return "Error occurred while fetching the last row."

    

    def insertRow(self, user_input:str, model_prediction:str, user_satisfaction_level:int, user_suggestion:str):
        query = f"""INSERT INTO {config.DB_NAME} ('user_input', 'prediction', 'user_satisfaction_level', 'suggestions')
                    VALUES ({user_input}, {model_prediction}, {user_satisfaction_level}, {user_suggestion})"""
        self.cursor.execute(query)
        self.db.commit()
        logging.info(f"Data insertion successfull = {user_input}, {model_prediction}, {user_satisfaction_level}, {user_suggestion}...")


    
    def deleteLast(self):
        """Deletes the last row based on the highest ID (assuming ID is the primary key)."""

        try:
            query = f"""DELETE FROM {config.DB_NAME} 
                        WHERE ID = (SELECT MAX(ID) FROM {config.DB_NAME})"""
            self.cursor.execute(query)
            self.db.commit()
            logging.info("Last row deleted successfully.")
        except Exception as e:
            logging.error(f"Failed to delete the last row: {e}")


    
    def replaceLastIfSame(self, user_input:str, model_prediction:str, user_satisfaction_level:int, user_suggestion:str):
        """Replace last row of database if latest user_input is same as last user_input"""

        last_user_input = self.readLast()['user_input']
        if user_input == last_user_input:
            self.deleteLast()
            self.insertRow(user_input=user_input, 
                            model_prediction=model_prediction, 
                            user_satisfaction_level=user_satisfaction_level, 
                            user_suggestion=user_suggestion)



    def findInDB(self, user_input:str) -> str:
        """Find given user_input in database, and return model prediction for that perticular input text
            This techniques will help me to reduce the cost of prediction and time consumption too."""
        
        query = f"""SELECT `prediction' FROM {config.DB_NAME}
                    WHERE 'user_input' = {user_input}"""
        self.cursor(query)
        prediction = self.cursor.fetchone()
        return prediction













