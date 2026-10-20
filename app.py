import base64
import codecs
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None
    use_rot13 = request.form.get("rot13") == "on"

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "encode":
            text = request.form.get("text", "")
            if use_rot13:
                text = codecs.encode(text, "rot_13")
            result = base64.b64encode(text.encode("utf-8")).decode("ascii")

        elif action == "decode":
            try:
                result = base64.b64decode(
                    request.form.get("text", ""), validate=True
                ).decode("utf-8")
                if use_rot13:
                    result = codecs.encode(result, "rot_13")
            except (ValueError, UnicodeDecodeError):
                error = "Stringa Base64 non valida o contenuto non UTF-8."

    return render_template(
        "home.html",
        error=error,
        result=result,
        text=request.form.get("text", ""),
        use_rot13=use_rot13,
    )


if __name__ == "__main__":
    app.run(debug=False)
