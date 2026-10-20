import base64
import codecs
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
                    delimiter = request.form.get("delimiter", ",")
                    if delimiter not in [",", ";", "\t", "|"]:
                        delimiter = ","
                    data = list(csv.reader(io.StringIO(uploaded.read().decode("utf-8-sig")),
                                           delimiter=delimiter))
                    if data:
                        headers, rows = data[0], data[1:101]
                    else:
                        error = "Il file CSV è vuoto."
                except (UnicodeDecodeError, csv.Error):
                    error = "File CSV non valido."
        elif action == "encode":
            text = request.form.get("text", "")
            rotated = codecs.encode(text, "rot_13")
            result = base64.b64encode(rotated.encode("utf-8")).decode("ascii")
        elif action == "decode":
            try:
                decoded = base64.b64decode(request.form.get("text", ""), validate=True).decode("utf-8")
                result = codecs.encode(decoded, "rot_13")
            except (ValueError, UnicodeDecodeError):
                error = "Stringa Base64 non valida o contenuto non UTF-8."
    return render_template("home.html", error=error, result=result, headers=headers,
                           rows=rows, text=request.form.get("text", ""))

if __name__ == "__main__":
    app.run(debug=False)
