from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import cv2
import time

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to a secure random key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Hardcoded user (replace with database in production)
users = {"admin": {"password": "admin123"}}

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

# Variables to control the trigger status
last_trigger_time = 0
TRIGGER_DURATION = 7  # seconds during which the live feed should be visible

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and password == users[username]["password"]:
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/trigger', methods=['POST'])
@login_required
def trigger():
    global last_trigger_time
    try:
        data = request.get_json()
        if not data:
            print("🚨 No JSON payload received!")
            return jsonify({"status": "error", "message": "No JSON payload"}), 400
        
        print(f"🚨 Trigger received from ESP32: {data}")
        last_trigger_time = time.time()
        return jsonify({"status": "success", "message": "Trigger received"}), 200
    except Exception as e:
        print(f"🚨 Error processing trigger: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/status')
@login_required
def status():
    if time.time() - last_trigger_time < TRIGGER_DURATION:
        return jsonify(triggered=True)
    else:
        return jsonify(triggered=False)

# --- Webcam Feed Setup ---
camera = cv2.VideoCapture(0)  # Adjust camera index if necessary (0 for default webcam)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            print("⚠️ Failed to capture frame from camera.")
            break
        else:
            # Optionally, add a timestamp overlay:
            cv2.putText(frame, time.strftime("%Y-%m-%d %H:%M:%S"),
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("⚠️ Failed to encode frame.")
                continue
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
@login_required
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
