from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import google.generativeai as genai

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
# FLASK
# =========================

app = Flask(__name__)

# =========================
# TEMP SENSOR DATA
# =========================

sensor_data = {

    "ph": 0,

    "temperature": 0,

    "soil_moisture": 0,

    "air_humidity": 0,

    "light": 0
}

# =========================
# HOME
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

    return render_template(
        "questions.html"
    )

# =========================
# RECOMMENDATION YES
# =========================

@app.route("/Rekomendasi_yes")
def recommendation_yes():

    # =========================
    # GET DATA FROM QUESTION
    # =========================

    fertilizer = request.args.get(
        "fertilizer",
        "Tidak Ada Data"
    )

    fertilizer_frequency = request.args.get(
        "fertilizer_frequency",
        "Tidak Ada Data"
    )

    vitamin = request.args.get(
        "vitamin",
        "Tidak Ada Data"
    )

    watering = request.args.get(
        "watering",
        "Tidak Ada Data"
    )

    # =========================
    # AI CONFIG
    # =========================

    USE_AI = False

    # =========================
    # AI PROMPT
    # =========================

    prompt = f"""

    Anda adalah AI pertanian modern.

    Analisis kondisi tanah berikut:

    Data Sensor:
    - pH tanah: {sensor_data["ph"]}
    - Suhu: {sensor_data["temperature"]}
    - Kelembaban tanah: {sensor_data["soil_moisture"]}
    - Kelembaban udara: {sensor_data["air_humidity"]}
    - Intensitas cahaya: {sensor_data["light"]}

    Riwayat Perawatan:
    - Jenis pupuk: {fertilizer}
    - Intensitas pemupukan: {fertilizer_frequency}
    - Vitamin tanaman: {vitamin}
    - Intensitas penyiraman: {watering}

    Buat analisis singkat maksimal 3 kalimat.
    Gunakan bahasa modern dan profesional.
    """

    # =========================
    # GEMINI RESPONSE
    # =========================

    if USE_AI:

        try:

            response = model.generate_content(
                prompt
            )

            recommendation = response.text

        except Exception as e:

            recommendation = f"""
            AI recommendation sementara tidak tersedia.
            Error:
            {str(e)}
            """

    else:

        recommendation = """
        Sistem AI sedang dinonaktifkan sementara 
        selama proses pengujian dashboard.
        """
    # =========================
    # SMART ACTIONS
    # =========================

    actions = []

    # =========================
    # SOIL MOISTURE
    # =========================

    if sensor_data["soil_moisture"] < 30:

        actions.append({

            "title":
            "Tingkatkan Kelembapan Tanah",

            "detail":
            "Lakukan penyiraman tambahan atau gunakan mulsa untuk menjaga kelembapan tanah lebih stabil."

        })

    elif sensor_data["soil_moisture"] > 70:

        actions.append({

            "title":
            "Perbaiki Drainase Tanah",

            "detail":
            "Kurangi intensitas penyiraman dan pastikan sistem drainase berjalan baik agar akar tidak membusuk."

        })

    # =========================
    # TEMPERATURE
    # =========================

    if sensor_data["temperature"] > 30:

        actions.append({

            "title":
            "Kurangi Paparan Panas Berlebih",

            "detail":
            "Gunakan naungan tambahan dan tingkatkan frekuensi penyiraman untuk mengurangi stres panas pada tanaman."

        })

    elif sensor_data["temperature"] < 20:

        actions.append({

            "title":
            "Jaga Suhu Lingkungan Tanaman",

            "detail":
            "Pindahkan tanaman ke area yang lebih hangat atau gunakan pelindung untuk menjaga suhu tetap stabil."

        })

    # =========================
    # SOIL PH
    # =========================

    if sensor_data["ph"] < 5.5:

        actions.append({

            "title":
            "Tingkatkan pH Tanah",

            "detail":
            "Tambahkan dolomit atau kapur pertanian untuk membantu menaikkan pH tanah agar lebih optimal bagi pertumbuhan tanaman."

        })

    elif sensor_data["ph"] > 7.5:

        actions.append({

            "title":
            "Turunkan pH Tanah",

            "detail":
            "Gunakan kompos, pupuk organik, atau belerang untuk membantu menurunkan pH tanah secara bertahap."

        })

    # =========================
    # LIGHT INTENSITY
    # =========================

    if sensor_data["light"] < 10000:

        actions.append({

            "title":
            "Tingkatkan Paparan Cahaya",

            "detail":
            "Pindahkan tanaman ke area yang lebih terbuka agar memperoleh cahaya matahari yang cukup."

        })

    elif sensor_data["light"] > 50000:

        actions.append({

            "title":
            "Kurangi Intensitas Cahaya Berlebih",

            "detail":
            "Gunakan paranet atau peneduh untuk mengurangi paparan cahaya langsung yang berlebihan."

        })

    # =========================
    # AIR HUMIDITY
    # =========================

    if sensor_data["air_humidity"] < 40:

        actions.append({

            "title":
            "Tingkatkan Kelembapan Udara",

            "detail":
            "Lakukan penyemprotan kabut air (misting) atau tambahkan sumber kelembapan di sekitar tanaman."

        })

    elif sensor_data["air_humidity"] > 70:

        actions.append({

            "title":
            "Tingkatkan Sirkulasi Udara",

            "detail":
            "Perbaiki ventilasi area tanam untuk mencegah pertumbuhan jamur dan penyakit pada tanaman."

        })

    # =========================
    # DEFAULT
    # =========================

    if len(actions) == 0:

        actions.append({

            "title":
            "Kondisi Tanaman Optimal",

            "detail":
            "Seluruh parameter lingkungan berada pada kondisi ideal untuk mendukung pertumbuhan tanaman."

        })

    # =========================
    # RENDER PAGE
    # =========================

    return render_template(

        "Rekomendasi_yes.html",
        

        recommendation=recommendation,

        actions=actions,

        fertilizer=fertilizer,

        fertilizer_frequency=fertilizer_frequency,

        vitamin=vitamin,

        watering=watering,

        ph=sensor_data["ph"],

        temperature=sensor_data["temperature"],

        soil_moisture=sensor_data["soil_moisture"],

        air_humidity=sensor_data["air_humidity"],

        light=sensor_data["light"]

    )

# =========================
# RECOMMENDATION NO
# =========================

@app.route("/recommendation-no")
def recommendation_no():

    # =========================
    # AI CONFIG
    # =========================

    USE_AI = False

    # =========================
    # AI PROMPT
    # =========================

    prompt = f"""

    Anda adalah AI pertanian modern.

    Analisis kondisi tanah berikut:

    Data Sensor:
    - pH tanah: {sensor_data["ph"]}
    - Suhu: {sensor_data["temperature"]}
    - Kelembaban tanah: {sensor_data["soil_moisture"]}
    - Kelembaban udara: {sensor_data["air_humidity"]}
    - Intensitas cahaya: {sensor_data["light"]}


    Buat analisis singkat maksimal 3 kalimat.
    Gunakan bahasa modern dan profesional.
    """

    # =========================
    # GEMINI RESPONSE
    # =========================

    if USE_AI:

        try:

            response = model.generate_content(
                prompt
            )

            recommendation = response.text

        except Exception as e:

            recommendation = f"""
            AI recommendation sementara tidak tersedia.
            Error:
            {str(e)}
            """

    else:

        recommendation = """
        Sistem AI sedang dinonaktifkan sementara 
        selama proses pengujian dashboard.
        """
    # =========================
    # SMART ACTIONS
    # =========================

    actions = []

    # =========================
    # SOIL MOISTURE
    # =========================

    if sensor_data["soil_moisture"] < 30:

        actions.append({

            "title":
            "Tingkatkan Kelembapan Tanah",

            "detail":
            "Lakukan penyiraman tambahan atau gunakan mulsa untuk menjaga kelembapan tanah lebih stabil."

        })

    elif sensor_data["soil_moisture"] > 70:

        actions.append({

            "title":
            "Perbaiki Drainase Tanah",

            "detail":
            "Kurangi intensitas penyiraman dan pastikan sistem drainase berjalan baik agar akar tidak membusuk."

        })

    # =========================
    # TEMPERATURE
    # =========================

    if sensor_data["temperature"] > 30:

        actions.append({

            "title":
            "Kurangi Paparan Panas Berlebih",

            "detail":
            "Gunakan naungan tambahan dan tingkatkan frekuensi penyiraman untuk mengurangi stres panas pada tanaman."

        })

    elif sensor_data["temperature"] < 20:

        actions.append({

            "title":
            "Jaga Suhu Lingkungan Tanaman",

            "detail":
            "Pindahkan tanaman ke area yang lebih hangat atau gunakan pelindung untuk menjaga suhu tetap stabil."

        })

    # =========================
    # SOIL PH
    # =========================

    if sensor_data["ph"] < 5.5:

        actions.append({

            "title":
            "Tingkatkan pH Tanah",

            "detail":
            "Tambahkan dolomit atau kapur pertanian untuk membantu menaikkan pH tanah agar lebih optimal bagi pertumbuhan tanaman."

        })

    elif sensor_data["ph"] > 7.5:

        actions.append({

            "title":
            "Turunkan pH Tanah",

            "detail":
            "Gunakan kompos, pupuk organik, atau belerang untuk membantu menurunkan pH tanah secara bertahap."

        })

    # =========================
    # LIGHT INTENSITY
    # =========================

    if sensor_data["light"] < 10000:

        actions.append({

            "title":
            "Tingkatkan Paparan Cahaya",

            "detail":
            "Pindahkan tanaman ke area yang lebih terbuka agar memperoleh cahaya matahari yang cukup."

        })

    elif sensor_data["light"] > 50000:

        actions.append({

            "title":
            "Kurangi Intensitas Cahaya Berlebih",

            "detail":
            "Gunakan paranet atau peneduh untuk mengurangi paparan cahaya langsung yang berlebihan."

        })

    # =========================
    # AIR HUMIDITY
    # =========================

    if sensor_data["air_humidity"] < 40:

        actions.append({

            "title":
            "Tingkatkan Kelembapan Udara",

            "detail":
            "Lakukan penyemprotan kabut air (misting) atau tambahkan sumber kelembapan di sekitar tanaman."

        })

    elif sensor_data["air_humidity"] > 70:

        actions.append({

            "title":
            "Tingkatkan Sirkulasi Udara",

            "detail":
            "Perbaiki ventilasi area tanam untuk mencegah pertumbuhan jamur dan penyakit pada tanaman."

        })

    # =========================
    # DEFAULT
    # =========================

    if len(actions) == 0:

        actions.append({

            "title":
            "Kondisi Tanaman Optimal",

            "detail":
            "Seluruh parameter lingkungan berada pada kondisi ideal untuk mendukung pertumbuhan tanaman."

        })

    # =========================
    # RENDER PAGE
    # =========================

    return render_template(

        "Rekomendasi_no.html",
        

        recommendation=recommendation,

        actions=actions,
        
        ph=sensor_data["ph"],

        temperature=sensor_data["temperature"],

        soil_moisture=sensor_data["soil_moisture"],

        air_humidity=sensor_data["air_humidity"],

        light=sensor_data["light"]

    )

@app.route("/sensor-data", methods=["POST"])
def receive_sensor_data():

    global sensor_data

    data = request.get_json()

    print("DATA MASUK:")
    print(data)

    sensor_data["ph"] = data["ph"]

    sensor_data["temperature"] = data["temperature"]

    sensor_data["soil_moisture"] = data["soil_moisture"]

    sensor_data["air_humidity"] = data["air_humidity"]

    sensor_data["light"] = data["light"]

    print("UPDATE SENSOR:")
    print(sensor_data)

    return jsonify({
        "message": "Data received successfully"
    })
# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":

    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)