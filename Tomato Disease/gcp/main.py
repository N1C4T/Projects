from functions_framework import http
import logging
from flask import jsonify, make_response

# Setup logging
logging.basicConfig(level=logging.INFO)

model = None
BUCKET_NAME = "nijat-tf-models"
MODEL_PATH = "models/tomatoes.h5"

class_names = [
    'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
    'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot', 'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus', 'Tomato_healthy'
]

@http
def predict(request):
    global model
    try:
        import tensorflow as tf
        from PIL import Image
        import numpy as np
        from google.cloud import storage
        import os

        logging.info("Predict request received.")

        if model is None:
            logging.info("Loading model from GCS...")
            storage_client = storage.Client()
            bucket = storage_client.bucket(BUCKET_NAME)
            blob = bucket.blob(MODEL_PATH)

            local_model_path = "/tmp/tomatoes.h5"
            blob.download_to_filename(local_model_path)
            logging.info("Model downloaded successfully.")

            model = tf.keras.models.load_model(local_model_path, compile=False)
            logging.info("Model loaded successfully.")

        if "file" not in request.files:
            return {"error": "No file provided"}, 400

        # Preprocessing image
        image_file = request.files["file"]
        image = Image.open(image_file).convert("RGB")
        image = np.array(image)
        img_array = tf.expand_dims(image, 0)

        # Predicting
        predictions = model.predict(img_array)
        predicted_class = class_names[int(np.argmax(predictions[0]))]
        confidence = float(round(100 * float(np.max(predictions[0])), 2))

        response = make_response(
            jsonify({"Class": predicted_class, "Confidence": float(confidence)})
        )
        # Allowing requests from any origin
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    except Exception as e:
        logging.exception("Error during prediction:")
        return {"error": str(e)}, 500
