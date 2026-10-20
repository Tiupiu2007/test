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
    action = request.form.get("action", "")

    if request.method == "POST" and action == "csv":
        uploaded = request.files.get("file")
        if uploaded is None or not uploaded.filename:
            error = "Seleziona un file CSV."
        else:
            try:
                content = uploaded.read().decode("utf-8-sig")
                delimiter = request.form.get("delimiter", ",")
                if delimiter not in [",", ";", "\t", "|"]:
                    delimiter = ","
                data = list(csv.reader(io.StringIO(content), delimiter=delimiter))
                if data:
                    headers, rows = data[0], data[1:101]
                else:
                    error = "Il file CSV è vuoto."
            except (UnicodeDecodeError, csv.Error):
                error = "Non riesco a leggere questo CSV. Prova un file UTF-8."

    elif request.method == "POST" and action in ("encode", "decode"):
        value = request.form.get("text", "")
        try:
            if action == "encode":
                result = base64.b64encode(value.encode("utf-8")).decode("ascii")
            else:
                result = base64.b64decode(value, validate=True).decode("utf-8")
        except Exception:
            error = "Base64 non valido oppure il contenuto decodificato non è testo UTF-8."

    return render_template("index.html", error=error, result=result,
                           headers=headers, rows=rows, action=action,
                           text=request.form.get("text", ""))


if __name__ == "__main__":
    app.run(debug=False)
