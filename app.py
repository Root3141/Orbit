from flask import Flask, jsonify, render_template, request
from sim import create_solar_system, sim_step, coordinates, SolarSystem, Star, Planet

app = Flask(__name__)

solar_system = None
dt = 60 * 60 * 24

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    global solar_system
    if solar_system is None:
        return jsonify({"error": "Simulation not initialized"}), 400
    sim_step(solar_system, dt)
    bodies = coordinates(solar_system)
    return jsonify(bodies)

@app.route("/init", methods=["POST"])
def init_sim():
    global solar_system
    selectedBodies = request.get_json()
    solar_system = create_solar_system(include=[b["label"] for b in selectedBodies])
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
