from flask import Flask, jsonify, render_template, request
from modbus_utils import read_modbus_data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  

@app.route("/read", methods=["GET"])
def read():
    unit_id = int(request.args.get("unit", 1))
    data = read_modbus_data(unit_id=unit_id)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
