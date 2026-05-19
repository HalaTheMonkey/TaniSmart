from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

# TEMPORARY STORAGE
sensor_data = {
    "ph": 0,
    "temperature": 0,
    "soil_moisture": 0,
    "air_humidity": 0,
    "light": 0
}

# ROUTE HOME
@app.route("/")
def home():

    return f"""
    <h1>Data Sensor</h1>

    <p>pH: {sensor_data['ph']}</p>
    <p>Suhu: {sensor_data['temperature']}</p>
    <p>Kelembapan Tanah: {sensor_data['soil_moisture']}</p>
    <p>Kelembapan Udara: {sensor_data['air_humidity']}</p>
    <p>Cahaya: {sensor_data['light']}</p>
    """

# ROUTE MENERIMA DATA DARI ESP32
@app.route("/sensor-data", methods=["POST"])
def receive_sensor_data():

    global sensor_data

    data = request.json

    sensor_data["ph"] = data["ph"]
    sensor_data["temperature"] = data["temperature"]
    sensor_data["soil_moisture"] = data["soil_moisture"]
    sensor_data["air_humidity"] = data["air_humidity"]
    sensor_data["light"] = data["light"]

    return jsonify({
        "message": "Data received successfully"
    })

# RUN FLASK
if __name__ == "__main__":

    app.run(debug=True)