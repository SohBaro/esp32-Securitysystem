# ESP32 Smart Surveillance System 

![Arduino](https://img.shields.io/badge/Firmware-C%2B%2B%20%7C%20Arduino-blue)
![Python](https://img.shields.io/badge/Backend-Flask%20%7C%20Python-yellow)
![Hardware](https://img.shields.io/badge/Hardware-ESP32--CAM-red)

An IoT-based security solution that transforms an ESP32 into a smart surveillance device. The system integrates **Ultrasonic** and **Sound sensors** to detect intruders, triggers a local alarm, and streams live video feed to a secure web dashboard.

---

## 🌟 Key Features

* **Live Video Streaming:** Real-time MJPEG stream from the ESP32-CAM to a Python Flask server.
* **Multi-Sensor Detection:**
    * **Motion:** HC-SR04 Ultrasonic sensor detects physical proximity/movement.
    * **Audio:** Sound sensor triggers alerts based on noise levels.
* **Active Deterrence:** Immediate buzzer activation upon intrusion detection.
* **Web Dashboard:** A responsive interface (HTML/CSS) to view the feed and monitor status.
* **Remote Access Capable:** Compatible with Cloudflare Tunnels for secure global access.

---

## 🛠️ Hardware Requirements

| Component | Description |
|-----------|-------------|
| **ESP32-CAM** | The main microcontroller with a camera module (AI-Thinker model recommended). |
| **FTDI Programmer** | To flash code onto the ESP32-CAM. |
| **HC-SR04** | Ultrasonic sensor for distance/motion measurement. |
| **Sound Sensor** | Microphone module (e.g., KY-037 or KY-038). |
| **Buzzer** | Active buzzer for the alarm. |
| **Power Supply** | 5V DC power source. |

---

##  Technical Architecture

The project operates in a client-server model:

1.  **The Edge Device (ESP32):** Captures video and sensor data. It acts as a local IP camera server.
2.  **The Backend (Python/Flask):** connects to the ESP32's stream, processes the data, and serves the web interface.
3.  **The Frontend (HTML):**
    * `index.html`: Main surveillance dashboard.
    * `login.html`: Secure entry point for the system.

---

##  Installation & Setup

### 1. Firmware Setup (Arduino IDE)
1.  Open the `.ino` file in **Arduino IDE**.
2.  Install the **ESP32 Board Manager** (Espressif Systems).
3.  **Configuration:**
    * Locate the `ssid` and `password` variables. Update them with your WiFi credentials.
    * Ensure the pin definitions match your physical wiring.
4.  Upload the code to the ESP32-CAM.
5.  Open the Serial Monitor (Baud Rate 115200) to find the **ESP32's Local IP Address** (e.g., `192.168.1.X`).

### 2. Backend Setup (Python)
Ensure you have Python installed.

```bash
# 1. Install dependencies
pip install flask opencv-python requests numpy

# 2. Update the IP Configuration
# Open app.py and replace the IP address placeholder with the ESP32 IP you found in step 1.

# 3. Run the Server
python app.py
```

### 3. Access the Dashboard
Open your browser and navigate to: http://127.0.0.1:5000 (or the port specified in your Flask app).

## 🌐 Remote Deployment (Optional)
Currently, the system runs on Localhost. To access the camera feed from anywhere in the world without port forwarding, we recommend using Cloudflare Tunnels.

Steps:

Install cloudflared on your host machine.

Create a Tunnel pointing to your local Flask port (e.g., 5000).

Map it to a domain name.

Video Tutorial:
https://youtu.be/BnWfbv7Fy-k?feature=shared
