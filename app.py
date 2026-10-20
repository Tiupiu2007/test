import base64
import csv
import io
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None
    headers = []
    rows = []
    if request.method == "POST":
        action = request.form.get("action", "")
        if action == "csv":
            uploaded = request.files.get("file")
            if not uploaded or not uploaded.filename:
                error = "Seleziona un file CSV."
            else:
                try:
                    data = list(csv.reader(io.StringIO(uploaded.read().decode("utf-8-sig")),
                                           delimiter=request.form.get("delimiter", ",")))
                    if data:
                        headers, rows = data[0], data[1:101]
                    else:
                        error = "Il file CSV è vuoto."
                except (UnicodeDecodeError, csv.Error):
                    error = "File CSV non valido."
        elif action == "encode":
            result = base64.b64encode(request.form.get("text", "").encode()).decode()
        elif action == "decode":
            try:
                result = base64.b64decode(request.form.get("text", ""), validate=True).decode()
            except (ValueError, UnicodeDecodeError):
                error = "Stringa Base64 non valida."
    return render_template("home.html", error=error, result=result, headers=headers,
                           rows=rows, text=request.form.get("text", ""))

if __name__ == "__main__":
    app.run(debug=False)
