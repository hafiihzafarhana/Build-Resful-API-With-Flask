from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def hai():
    return jsonify({"Status": "SUCCESS", "Message": "Success to get endpoint", "Data": {"nama": "Hafi"}})
