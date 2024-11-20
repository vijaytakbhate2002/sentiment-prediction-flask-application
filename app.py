import logging
from flask import Flask, request, render_template, redirect
from sentiment_prediction import predict  
from db_operations.db_handling import DatabaseOperations
from text_operations import emojis_remover

logging.basicConfig(
    filename='logs.log',        
    filemode='a',               
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO          
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
    user_input = emojis_remover.remove_emojis(user_input)

    if user_input == None:
        return home(model_prediction=None, user_input=None)
    
    logging.info(f"user_input = {user_input}")

    model_prediction = predict.predictor(user_input)[0]
    logging.info(f"predicted sentiment = {model_prediction}")

    db_operations.insertRow(user_input=user_input, 
                            model_prediction=model_prediction, 
                            user_satisfaction_level=None, 
                            user_suggestion=None)
    
    logging.info(f"New entry to database {user_input}, {model_prediction}")

    return home(model_prediction=model_prediction, user_input=user_input)



@app.route('/feedback', methods=['POST'])
def feedback():
    user_satisfaction_level = request.form['user_satisfaction']
    user_suggestion = request.form['user_suggestion']

    db_operations.updateLastRow(user_satisfaction_level=user_satisfaction_level,
                                user_suggestion=user_suggestion)

    logging.info("Feedback and suggestions updated for the latest input.")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
