"""Flask web app for the DataPilot CSV quality demo."""

import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from data_processor import analyze_csv

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


@app.get("/
def index():
    return render_template("index.html")


@app.post("/analyze")
def analyze():
    uploaded = request.files.get("file")
    delimiter = request.form.get("delimiter", ",")
    if delimiter not in {",", ";", "\\t", "|"}:
        delimiter = ","
    if uploaded is None or not uploaded.filename:
        return render_template("index.html", error="Seleziona prima un file CSV."), 400
    filename = secure_filename(uploaded.filename)
    if not filename.lower().endswith(".csv"):
        return render_template("index.html", error="Carica un file con estensione .csv."), 400
    try:
        content = uploaded.stream.read().decode("utf-8-sig")
        report = analyze_csv(content, delimiter=delimiter)
    except UnicodeDecodeError:
        return render_template("index.html", error="Il file deve essere codificato in UTF-8."), 400
    except ValueError as exc:
        return render_template("index.html", error=str(exc)), 400
    return render_template("results.html", report=report, filename=filename)


@app.errorhandler(413)
def file_too_large(_error):
    return render_template("index.html", error="Il file supera il limite di 5 MB."), 413


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
