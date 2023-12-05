import numpy as np
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
from joblib import load

app = Flask(__name__)

scaler_x = load('scaler_x.pkl')
scaler_y = load('scaler_y.pkl')

model = load_model('model (1).h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # input pengguna
        wind_speed = float(request.form['wind_speed'])
        wind_direction = float(request.form['wind_direction'])
        input_array = np.array([[wind_speed, wind_direction]])
        input_array = scaler_x.transform(input_array)
        input_array = input_array.reshape((1, input_array.shape[0], input_array.shape[1]))

        # predict
        predictions = model.predict(input_array)
        predictions_denorm = scaler_y.inverse_transform(predictions)
        prediction_result = float(predictions_denorm[0][0])
        result = {'prediction': prediction_result}

        return render_template('index.html', prediction=result['prediction'])

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('index.html', prediction_error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
