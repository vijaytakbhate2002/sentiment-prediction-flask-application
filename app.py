import logging
from flask import Flask, request, render_template, redirect
from sentiment_prediction import predict  
from db_operations.db_handling import DatabaseOperations


logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
    handlers=[
        logging.FileHandler('app.log'),  
        logging.StreamHandler() 
    ]
)

db_operations = DatabaseOperations()


model_prediction = None
user_input = None
app = Flask(__name__)



@app.route('/')
def home(model_prediction=model_prediction, user_input=user_input):
    return render_template('index.html', model_prediction=model_prediction, user_input=user_input)



@app.route('/prediction', methods=['POST'])
def prediction():
    """predict sentiment for user input which is came from index.html page from user
        insert into last row"""
    
    logging.info("Reading user input ...")
    user_input = request.form['user_input']
    logging.info(f"user_input = {user_input}")
    
    model_prediction = predict.predictor(user_input) 
    logging.info(f"predicted sentiment = {model_prediction}")

    db_operations.insertRow(user_input=user_input, 
                            model_prediction=model_prediction, 
                            user_satisfaction_level=None, 
                            user_suggestion=None)
    
    logging.info(f"New entry to database {user_input}, {model_prediction}")

    return home(model_prediction=model_prediction, user_input=user_input)



@app.route('/feedback', methods=['POST'])
def feedback():

    user_satisfaction_level = request.form['feedback']
    user_suggestion = request.form['suggestions']

    db_operations.replaceLastIfSame(user_input=user_input, 
                            model_prediction=model_prediction, 
                            user_satisfaction_level=user_satisfaction_level, 
                            user_suggestion=user_suggestion)

    logging.info("Feedback and suggestions updated for the latest input.")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
