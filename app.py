from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb+srv://al222410839_db_user:fernando.123@cluster0.5x95bfb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["portal_distintivos"]
collection = db["registros"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/distintivos", methods=["GET"])
def get_distintivos():
    return jsonify(list(collection.find({}, {"_id": False})))

@app.route("/api/distintivos/actualizar", methods=["POST"])
def actualizar_distintivo():
    req_data = request.json
    collection.update_one(
        {"FOLIO": req_data.get("FOLIO")},
        {"$set": req_data},
        upsert=True
    )
    return jsonify({"success": True, "message": "Actualizado"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)