from flask import Flask, request, render_template, send_from_directory
import os
import uuid
from engine import run_match
import json

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
MATCH_FOLDER = "matches"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MATCH_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        bot1 = request.files["bot1"]
        bot2 = request.files["bot2"]

        bot1_path = os.path.join(UPLOAD_FOLDER, f"bot1_{uuid.uuid4().hex}.py")
        bot2_path = os.path.join(UPLOAD_FOLDER, f"bot2_{uuid.uuid4().hex}.py")

        bot1.save(bot1_path)
        bot2.save(bot2_path)

        match_result = run_match(bot1_path, bot2_path)
        match_id = uuid.uuid4().hex
        match_file = os.path.join(MATCH_FOLDER, f"{match_id}.json")
        with open(match_file, "w") as f:
            json.dump(match_result, f)

        return render_template("index.html", match_id=match_id, result=match_result["result"])

    return render_template("index.html")

@app.route("/match/<match_id>")
def get_match(match_id):
    return send_from_directory(MATCH_FOLDER, f"{match_id}.json")

if __name__ == "__main__":
    app.run(debug=True)

