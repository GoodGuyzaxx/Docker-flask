from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

MODEL_PATH = 'model.pkl'
ENCODER_PATH = 'label_encoder.pkl'
REQUIRED_FEATURE_KEYS = ['suhu_udara', 'kelembaban_udara', 'kelembaban_tanah', 'intensitas_cahaya']

try:
    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)
    print("Model berhasil Diload")
except Exception as e:
    print(f"Error: {e}")
    model = None
    encoder = None

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if model is None or encoder is None:
        return jsonify({"error": "Model atau encoder tidak dimuat."}), 500

    try:
    
        data = request.get_json(force=True)

        if not data or not all(key in data for key in REQUIRED_FEATURE_KEYS):
            return jsonify({
                "status": "error",
                "error": "Data tidak lengkap. Pastikan semua fitur di isi."
            }), 400

        input_features = [data[key] for key in REQUIRED_FEATURE_KEYS]
        input_array = np.array([input_features])
        input_array = np.array([input_features])


        prediction_encoded = model.predict(input_array)
        prediction_label = encoder.inverse_transform(prediction_encoded)[0]


        prediction_proba = model.predict_proba(input_array)[0]
        probabilities = {class_label: f"{proba:.2f}" for class_label, proba in zip(encoder.classes_, prediction_proba)}

        return jsonify({
            'prediction': prediction_label,
            'probabilities': probabilities,
            'status': "success",
            'message': "Prediksi berhasil dilakukan."
        })

    except KeyError as e:
        return jsonify({
            "status": "error",
            "message": f"Data untuk fitur yang hilang: {e}"
        }), 400
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run()
