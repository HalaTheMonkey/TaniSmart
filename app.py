from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)

# =========================
# TEMPORARY SENSOR STORAGE
# =========================

sensor_data = {
    "ph": 6.5,
    "temperature": 37,
    "soil_moisture": 18,
    "air_humidity": 62,
    "light": 820
}

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    return render_template(

        "home.html",

        ph=sensor_data["ph"],
        temperature=sensor_data["temperature"],
        soil_moisture=sensor_data["soil_moisture"],
        air_humidity=sensor_data["air_humidity"],
        light=sensor_data["light"]

    )

# =========================
# QUESTION PAGE
# =========================

@app.route("/question")
def question():

    return render_template("questions.html")

# =========================
# RECOMMENDATION YES PAGE
# =========================

@app.route("/recommendation-yes")
def recommendation_yes():

    return render_template(

        "recommendation_yes.html",

        ph=sensor_data["ph"],
        temperature=sensor_data["temperature"],
        soil_moisture=sensor_data["soil_moisture"],
        air_humidity=sensor_data["air_humidity"],
        light=sensor_data["light"]

    )

# =========================
# RECOMMENDATION NO PAGE
# =========================

@app.route("/recommendation-no")
def recommendation_no():

    return render_template(

        "Rekomendasi_no.html",

        ph=sensor_data["ph"],
        temperature=sensor_data["temperature"],
        soil_moisture=sensor_data["soil_moisture"],
        air_humidity=sensor_data["air_humidity"],
        light=sensor_data["light"]

    )

# =========================
# RECEIVE SENSOR DATA
# FROM ESP32 / ARDUINO
# =========================

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

# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":

    app.run(debug=True)