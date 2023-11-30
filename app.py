from flask import Flask, render_template, request ,jsonify
import pickle
import json
from chat import get_response,predict_class
from my_web3 import Web3
from my_web3 import get_chatbot_interactions 
from my_web3 import add_chatbot_interaction



app = Flask(__name__)

intents = json.loads(open('intents.json').read())
# Load the machine learning model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
# Load the list of symptoms
with open('symptoms.txt', 'r') as f:
    symptoms = [line.strip() for line in f.readlines()]

# Define the index route
@app.route('/')
def index():
    # Render the index.html template with the list of symptoms
    return render_template('index.html', symptoms=symptoms)

#Define searching feature
@app.route('/search', methods=['POST'])
def search():
    word = request.form.get('search')
    with open('symptoms.txt', 'r') as f:
        symptoms = [line.strip() for line in f.readlines() if word in line]
    return render_template('index.html', symptoms=symptoms)

# Define the predict route
@app.route('/predict', methods=['POST'])
def predict():
    # Get the selected symptoms from the form
    selected_symptoms = [int(symptom) for symptom in request.form.getlist('symptoms')]
    # Create the input vector
    input_vector = [0] * 132
    for symptom in selected_symptoms:
        input_vector[symptom] = 1
    # Get the prediction from the model
    prediction = model.predict([input_vector])[0]
    # Get the list of class labels from the model
    class_labels = model.classes_
    # Find the index of the predicted class label
    prediction_index = list(class_labels).index(prediction)
    # Get the probability of the predicted class
    percentage = model.predict_proba([input_vector])[0][prediction_index] * 100
    return render_template('result.html', prediction=prediction, percentage=round(percentage,2))
   
@app.route('/chatbot', methods=['POST'])
def chatbot():
    text = request.get_json().get("message")
    ints = predict_class(text)    
    response = get_response(ints,intents)
    add_chatbot_interaction("user_id", text)
    message = {"answer": response}
    return jsonify(message) 


@app.route('/historical_interactions', methods=['GET'])
def historical_interactions():
    # Implement the logic to retrieve and display historical chatbot interactions from the smart contract
    interactions = get_chatbot_interactions()
    return render_template('historical_interactions.html', interactions=interactions)

    
if __name__ == '__main__':
    app.run(debug=True)




