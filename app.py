from flask import Flask, request, render_template
import logging
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.exception import CustomException
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

# Setup logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score'))
            )
            pred_df = data.get_data_as_data_frame()
            app.logger.info(f"Received data for prediction: {pred_df}")
            app.logger.info("Before Prediction")

            predict_pipeline = PredictPipeline()
            app.logger.info("Mid Prediction")
            results = predict_pipeline.predict(pred_df)
            app.logger.info("After Prediction")
            app.logger.info(f"Prediction results: {results}")

            return render_template('home.html', results=results[0])
        except Exception as e:
            app.logger.error("Error occurred during prediction", exc_info=True)
            return render_template('home.html', error=str(e))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")