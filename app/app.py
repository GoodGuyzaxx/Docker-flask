import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

@app.route("/")
def hello():
    return render_template("index.html")

# Load model
with open('cabai_rf_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.json
        features = [
            data['suhu_udara'], 
            data['kelembaban_udara'], 
            data['kelembaban_tanah'], 
            data['intensitas_cahaya']
        ]
        
        # Convert to numpy array
        input_data = np.array([features])
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0].tolist()
        
        # Return result
        return jsonify({
            'prediction': prediction,
            'probabilities': probabilities,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        })

if __name__ == '__main__':
    app.run()