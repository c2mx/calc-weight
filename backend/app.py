# backend/app.py

import os
import sys
from flask import Flask, request, render_template, send_file
# 确保当前目录加入 sys.path（如果需要）
sys.path.insert(0, os.path.dirname(__file__))
from original import process_file

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/calc", methods=["POST"])
def calc():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    upload_path = os.path.join("/tmp", "data.xlsx")
    result_path = os.path.join("/tmp", "result_data.xlsx")
    
    file.save(upload_path)
    process_file(input_path=upload_path, output_path=result_path)
    
    print("Output file exists:", os.path.exists(result_path))
    print("Output file path:", result_path)
    return send_file(result_path,
                 mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                 download_name="result_data.xlsx",
                 as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
