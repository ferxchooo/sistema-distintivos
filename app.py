from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

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
    registros = []
    for r in collection.find({}):
        r["_id"] = str(r["_id"]) # Convertimos el ID secreto a texto para la web
        registros.append(r)
    return jsonify(registros)

@app.route("/api/distintivos/actualizar", methods=["POST"])
def actualizar_distintivo():
    req_data = request.json
    record_id = req_data.get("_id")
    
    # Quitamos el ID de los datos para no confundir a MongoDB
    if "_id" in req_data:
        del req_data["_id"]
        
    if record_id:
        # Si ya existe, lo actualiza (¡Ahora puedes cambiar el folio libremente!)
        collection.update_one({"_id": ObjectId(record_id)}, {"$set": req_data})
    else:
        # Si es totalmente nuevo, lo crea
        collection.insert_one(req_data)
        
    return jsonify({"success": True})

# ¡NUEVA RUTA PARA ELIMINAR!
@app.route("/api/distintivos/eliminar", methods=["POST"])
def eliminar_distintivo():
    record_id = request.json.get("_id")
    if record_id:
        collection.delete_one({"_id": ObjectId(record_id)})
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
