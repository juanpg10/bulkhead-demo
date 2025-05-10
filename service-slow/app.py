from flask import Flask
import time
app = Flask(__name__)

@app.route('/')
def home():
    time.sleep(10)  # Simula servicio lento
    return "Servicio lento respondió", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')
