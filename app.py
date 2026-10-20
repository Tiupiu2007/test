from flask import Flask, render_template, request
from data_processor import analyze_csv

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    uploaded = request.files.get("file")
    if uploaded is None or not uploaded.filename or not uploaded.filename.lower().endswith(".csv"):
        return render_template("index.html", error="Seleziona un file CSV valido."), 400
    delimiter = request.form.get("delimiter", ",")
    if delimiter not in [",", ";", "\t", "|"]:
        delimiter = ","
    try:
        text = uploaded.read().decode("utf-8-sig")
        report = analyze_csv(text, delimiter)
    except (UnicodeDecodeError, ValueError) as exc:
        return render_template("index.html", error=str(exc) or "Formato non valido."), 400
    return render_template("results.html", report=report, filename=uploaded.filename)

if __name__ == "__main__":
    app.run(debug=False)
