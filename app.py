from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import google.generativeai as genai

# =========================
# FLASK
# =========================

app = Flask(__name__)

# =========================
# GEMINI API
# =========================

genai.configure(
    api_key="AIzaSyC2NtG6knHq5rUYO8GAMBIpOTqrOX-5th8"
)

model = genai.GenerativeModel(
     "gemini-2.5-flash"
)

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

@app.route("/Rekomendasi_yes")
def recommendation_yes():

    # =========================
    # GET USER INPUT
    # =========================

    fertilizer = request.args.get("fertilizer")

    fertilizer_frequency = request.args.get(
        "fertilizer_frequency"
    )

    vitamin = request.args.get("vitamin")

    watering = request.args.get("watering")

    notes = request.args.get("notes")

    # =========================
    # AI PROMPT
    # =========================

    prompt = f"""

    Kamu adalah AI pertanian pintar.

    Berikut kondisi tanah saat ini:

    pH tanah:
    {sensor_data["ph"]}

    Suhu:
    {sensor_data["temperature"]} derajat celcius

    Kelembapan tanah:
    {sensor_data["soil_moisture"]}%

    Kelembapan udara:
    {sensor_data["air_humidity"]}%

    Intensitas cahaya:
    {sensor_data["light"]}

    Riwayat perawatan pengguna:

    Jenis pupuk:
    {fertilizer}

    Intensitas pemberian pupuk:
    {fertilizer_frequency}

    Vitamin tanaman:
    {vitamin}

    Intensitas penyiraman:
    {watering}

    Catatan tambahan:
    {notes}

    Berikan rekomendasi perawatan tanah
    yang modern, singkat, jelas,
    mudah dipahami, dan terlihat profesional.

    Gunakan format poin-poin.

    """

    # =========================
    # GEMINI RESPONSE
    # =========================

    response = model.generate_content(prompt)

    recommendation = response.text

    # =========================
    # RENDER PAGE
    # =========================

    return render_template(

        "Rekomendasi_yes.html",

        recommendation=recommendation,

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

    prompt = f"""

    Kamu adalah AI pertanian pintar.

    Berikut kondisi tanah saat ini:

    pH tanah:
    {sensor_data["ph"]}

    Suhu:
    {sensor_data["temperature"]} derajat celcius

    Kelembapan tanah:
    {sensor_data["soil_moisture"]}%

    Kelembapan udara:
    {sensor_data["air_humidity"]}%

    Intensitas cahaya:
    {sensor_data["light"]}

    Pengguna tidak memiliki
    riwayat perawatan tanah.

    Berikan rekomendasi perawatan tanah
    yang modern, jelas,
    singkat, dan profesional.

    Gunakan format poin-poin.

    """

    response = model.generate_content(prompt)

    recommendation = response.text

    return render_template(

        "Rekomendasi_no.html",

        recommendation=recommendation,

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