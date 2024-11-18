import logging
import mysql.connector
from flask import Flask, request, render_template, redirect
from sentiment_prediction import predict  # Import your pre-built package
# from db_config import db_config  # Assuming you have a db_config in db_config.py for DB settings

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Define the log format
    handlers=[
        logging.FileHandler('app.log'),  # Log to a file named app.log
        logging.StreamHandler()  # Also log to console
    ]
)

sentiment = None
user_input = None
app = Flask(__name__)

@app.route('/')
def home(sentiment=sentiment, user_input=user_input):
    return render_template('index.html', sentiment=sentiment, user_input=user_input)

@app.route('/prediction', methods=['POST'])
def prediction():
    logging.info("User predict ...")
    user_input = request.form['user_input']
    logging.info(f"user_input ========================================= {user_input}")
    
    sentiment = predict.predictor(user_input) 
    logging.info(f"sentiment ========================================= {sentiment}")
    
    logging.info(f"New input added to the database: {user_input}, {sentiment}")
    return home(sentiment=sentiment, user_input=user_input)

@app.route('/feedback', methods=['POST'])
def feedback():
    feedback = request.form['feedback']
    suggestions = request.form['suggestions']
    
    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute("""
    # UPDATE UserInput SET feedback=%s, suggestion=%s 
    # WHERE id = (SELECT MAX(id) FROM UserInput)
    # """, (feedback, suggestions))
    # conn.commit()
    # cursor.close()
    # conn.close()

    logging.info("Feedback and suggestions updated for the latest input.")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
