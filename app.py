import os
import tensorflow as tf
from flask import Flask, request, redirect, url_for, render_template

from classifier import classify

app = Flask(__name__)

STATIC_FOLDER = "static"
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "uploads")
MODEL_PATH = os.path.join(STATIC_FOLDER, "models", "cat_dog.keras")

cnn_model = tf.keras.models.load_model(MODEL_PATH)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files.get("image")
        if file and file.filename:
            upload_image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(upload_image_path)
            return redirect(url_for("result", filename=file.filename))
    return render_template("index.html")


@app.route("/result")
def result():
    filename = request.args.get("filename")
    if not filename:
        return redirect(url_for("home"))

    image_path = os.path.join(UPLOAD_FOLDER, filename)

    label, prob = classify(cnn_model, image_path)
    prob = round((prob * 100), 2)

    return render_template("result.html", label=label, probability=prob,
                           image_url=url_for('static', filename=f'uploads/{filename}'))


if __name__ == "__main__":
    app.run(debug=True)
