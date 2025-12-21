import threading
import time

from drivers.coche_dc import Coche
from  utils.logger import Logger
from utils.robot_state import RobotState
from web_server import start_server, robot_shared_state

# Asumimos que estas son tus clases ya creadas
# from drivers.coche_dc import Coche 
# from utils.logger import Logger

# --- CLASE DE ESTADO COMPARTIDO ---

# --- HILO 1: ANALIZADOR DE COMANDOS (INPUT) ---
def console_thread(shared_state):
    print("--- SISTEMA LISTO ---")
    print("Comandos disponibles:")
    print("  start, stop, auto [x], manual")
    print("  adelante [x], atras [x], derecha [x], izquierda [x]")
    print("  velocidad [x], salir")
    
    while shared_state.running:
        try:
            # 1. Leer entrada del usuario (bloqueante)
            user_input = input("CMD >> ").strip().lower().split()
            
            if not user_input: continue
            
            cmd = user_input[0]
            val = int(user_input[1]) if len(user_input) > 1 else None

            # 2. Lógica de comandos
            if cmd == "salir":
                shared_state.running = False
                break
            
            elif cmd == "stop":
                shared_state.update(mode="STOP")
                print("-> PARADA DE EMERGENCIA")

            elif cmd == "start" or cmd == "manual":
                shared_state.update(mode="MANUAL")
                print("-> Modo Manual Activado")

            elif cmd == "auto":
                velocidad = val if val else 50
                shared_state.update(mode="AUTO", speed=velocidad)
                print(f"-> Modo Automático Activado a {velocidad}%")

            elif cmd in ["adelante", "atras", "derecha", "izquierda"]:
                # Si nos dan velocidad, actualizamos, si no, mantenemos la anterior
                shared_state.update(mode="MANUAL", command=cmd, speed=val)
                print(f"-> Ejecutando: {cmd} (Vel: {val if val else 'Mantener'})")
            
            elif cmd == "velocidad" and val is not None:
                shared_state.update(speed=val)
                print(f"-> Velocidad cambiada a {val}")

            else:
                print("Comando no reconocido.")

        except ValueError:
            print("Error: El valor debe ser un número (ej: 'adelante 50')")
        except Exception as e:
            print(f"Error en consola: {e}")

# --- HILO 2: LÓGICA DEL ROBOT (CONTROL LOOP) ---
def robot_logic_thread(shared_state, robot):
    print("Hilo del robot iniciado...")
    
    # Variable para recordar el último comando y no repetir acciones
    last_mode = None
    last_cmd = None
    
    while shared_state.running:
        # 1. Leer estado actual
        mode, cmd, speed = shared_state.get_state()
        
        # 2. Solo imprimimos si el modo ha cambiado (Para limpiar la consola)
        if mode != last_mode:
            print(f"\n[ROBOT] Cambio de modo: {last_mode} -> {mode}")
            # Si entramos en STOP, paramos una vez.
            if mode == "STOP":
                robot.detener()
        
        # 3. Lógica continua
        try:
            if mode == "STOP":
                # Por seguridad, aseguramos que siga parado, 
                # PERO tu clase 'detener' NO debe tener prints dentro.
                robot.detener() 

            elif mode == "MANUAL":
                # Solo actuamos si cambia el comando o el modo
                if cmd != last_cmd or mode != last_mode:
                    if cmd == "adelante":
                        robot.avanzar(speed)
                    elif cmd == "atras":
                        robot.retroceder(speed)
                    elif cmd == "derecha":
                        robot.girar_derecha(speed)
                    elif cmd == "izquierda":
                        robot.girar_izquierda(speed)
                    else:
                        robot.detener()

            elif mode == "AUTO":
                # Aquí SÍ queremos bucle continuo para leer sensores
                distancia = robot.sensor.medir_distancia()
                if distancia and 0 < distancia < 20:
                    #random elección de giro
                    import random
                    if random.choice([True, False]):
                        robot.girar_izquierda(50)
                    else:
                        robot.girar_derecha(50)

                else:
                    robot.avanzar(speed)

            # Actualizamos la memoria del estado anterior
            last_mode = mode
            last_cmd = cmd

            time.sleep(0.1)

        except Exception as e:
            print(f"Error: {e}")
            robot.detener()

# --- MAIN ---
def main():
    # 1. Cargar Configuración
    coche = Logger.load_config("./config/settings.json")
    
    # 2. Inicializar Hardware (Mock o Real)
    robot = coche  # Asumimos que Logger devuelve un objeto Coche ya inicializado
    


    # 4. Crear Hilos
    # Hilo de lógica (Daemon = se cierra si el programa principal se cierra a la fuerza)
    thread_logic = threading.Thread(target=robot_logic_thread, args=(robot_shared_state, robot))
    thread_logic.daemon = True 
    
    # 5. Arrancar
    thread_logic.start()
    print("-------Servidor web arrancado-------")
    print("Accede a la interfaz web en: http://192.168.8.1:5000")
    start_server(robot_shared_state) #ImportError: cannot import name 'start_server' from 'web_server' (/home/debian/app/src/web_server.py)

    
    # El hilo de consola corre en el hilo principal (Main Thread)
    # porque 'input()' a veces da problemas en hilos secundarios.
    console_thread(robot_shared_state)

    # 6. Esperar a que termine la lógica (cuando user escribe 'salir')
    thread_logic.join()
    print("Programa terminado.")

if __name__ == "__main__":
    main()