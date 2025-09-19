from flask import Flask, jsonify, render_template
from sim import create_solar_system, sim_step, coordinates

app = Flask(__name__)

solar_system = create_solar_system()
dt = 60 * 60 * 24

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    sim_step(solar_system, dt)
    bodies = coordinates(solar_system)
    return jsonify(bodies)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
