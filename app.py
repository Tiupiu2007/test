import base64
import codecs
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "encode":
            text = request.form.get("text", "")
            rotated = codecs.encode(text, "rot_13")
            result = base64.b64encode(rotated.encode("utf-8")).decode("ascii")

        elif action == "decode":
            try:
                decoded = base64.b64decode(
                    request.form.get("text", ""), validate=True
                ).decode("utf-8")
                result = codecs.encode(decoded, "rot_13")
            except (ValueError, UnicodeDecodeError):
                error = "Stringa Base64 non valida o contenuto non UTF-8."

    return render_template(
        "home.html",
        error=error,
        result=result,
        text=request.form.get("text", ""),
    )


if __name__ == "__main__":
    app.run(debug=False)
