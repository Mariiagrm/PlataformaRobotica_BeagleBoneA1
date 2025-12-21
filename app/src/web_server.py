from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import eventlet
import eventlet.wsgi
from utils.robot_state import RobotState

eventlet.monkey_patch() # Parchea las librerías estándar para que funcionen con eventlet

#Variables globales para el estado compartido
robot_shared_state = RobotState()

# Definimos variables globales para conectar con el main
server_app = Flask(__name__, template_folder='templates')
socketio = SocketIO(server_app, cors_allowed_origins="*", async_mode='eventlet')


@server_app.route('/')
def index():
    return render_template('index.html')

@socketio.on('comando')
def handle_command(json):
    raw_data = json['data'] # Recibe: "adelante 2000" o "stop 0"
    print(f"[WEB] Recibido crudo: {raw_data}")

    # 1. Separar el texto por espacios
    # "adelante 2000".split()  ->  ["adelante", "2000"]
    # "stop".split()           ->  ["stop"]
    parts = raw_data.split()
    
    cmd = parts[0] # La primera parte es el comando ("adelante")
    
    # 2. Si hay una segunda parte (la velocidad), la procesamos
    if len(parts) > 1:
        try:
            velocidad = int(parts[1]) # Convertimos "2000" a numero 2000
            if robot_shared_state:
                robot_shared_state.update(speed=velocidad)
        except ValueError:
            print("Error: La velocidad no es un número válido")

    # 3. Ejecutar el comando limpio
    if robot_shared_state:
        if cmd == "stop":
            # Nota: 'stop' suele ignorar la velocidad, así que da igual si viene o no
            robot_shared_state.update(command="stop")
        else:
            robot_shared_state.update(mode="MANUAL", command=cmd)

@socketio.on('velocidad')
def handle_speed(json):
    val = int(json['data'])
    if robot_shared_state:
        robot_shared_state.update(speed=val)

@socketio.on('modo_switch')
def handle_mode():
    if robot_shared_state:
        current_mode = robot_shared_state.get_state()[0]
        new_mode = "AUTO" if current_mode == "MANUAL" else "MANUAL"
        robot_shared_state.update(mode=new_mode)
        print(f"[WEB] Modo cambiado a {new_mode}")


def start_server(state_instance):
    global robot_shared_state
    robot_shared_state = state_instance
    # host='0.0.0.0' hace que sea accesible desde otros dispositivos en la red
    # SoftAp0: 192.168.8.1

    #socketio.run(server_app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
    #Permite multiples conexiones simultáneas con eventlet
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), server_app)
