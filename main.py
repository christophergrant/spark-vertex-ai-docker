from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
import pandas as pd
import numpy
import logging
import datetime

logging.basicConfig(level=logging.INFO)


class VertexAIPySparkModel:
    def __init__(self, model_path):
        pass
    def predict(self, pandas_df):
        """
        Note: input / output are both pandas dataframe.
        """
        spark_df = spark.createDataFrame(pandas_df)
        result_df = spark_pipeline_model.transform(spark_df)
        return result_df

app = Flask(__name__)
CORS(app)

#model_path saved locally
model_path = "sparkml"

#initialize model
spark_model = VertexAIPySparkModel(model_path)

# create spark local session
spark = SparkSession.builder.master("local").getOrCreate()
spark_pipeline_model = PipelineModel.load(model_path)


# Health check route
@app.route("/isalive")
def is_alive():
    print("/isalive request")
    status_code = Response(status=200)
    return status_code

# Predict route
@app.route("/predict", methods=["POST"])
def predict():
    print("/predict request")
    logging.info("REQUEST RECEIVED")
    now = datetime.datetime.now().isoformat()
    print(f"REQUEST RECEIVED {now}")
    req_json = request.get_json()
    
    
    pandas_df = pd.DataFrame(req_json)
    
    predict_df = spark_model.predict(pandas_df)

    result = predict_df.toJSON().first()
    
    logging.info("INFERENCE COMPLETE")
    now = datetime.datetime.now().isoformat()
    print(f"INFERENCE COMPLETE {now}")
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
