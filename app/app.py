from flask import Flask, render_template, Response, request, jsonify
from app.helpers.analize_board import analize_board
from app.utils.talk import say_movement
import cv2

app = Flask(__name__)
cap = cv2.VideoCapture("http://192.168.20.17:4747/video")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(analize_board(cap), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/say-movement', methods=['POST'])
def say_movement_rest():
    if request.method == 'POST':
        try:
            data = request.get_json()

            # Verifica si el JSON contiene la clave "mensaje"
            if 'mensaje' in data:
                mensaje = data['mensaje']
                say_movement(mensaje)
                return "OK"
            else:
                return jsonify({"error": "Formato JSON incorrecto. Se esperaba {'mensaje': 'texto'}"}), 400 
        except RuntimeError:
            return "Ya en reproducción"
    else:
        return "Invalid request method", 405

@app.route('/get-game-state')
def get_name_state():
    #Retorna el estado del juego, con la matriz y la validacion de si ha cambiado o no en un json
    return {
        "matrix": [
            ["", "", ""],
            ["", "C", ""],
            ["T", "C", ""]
        ],
        "changed": True
    }
    
    
