import time
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
# 2. Sube un nivel para llegar a la raíz del proyecto
root_dir = os.path.dirname(current_dir)

# 3. Añade la raíz a las rutas de búsqueda de Python
sys.path.insert(0, root_dir)
from src.utils.logger import Logger
 

from src.drivers.motor_dc import MotorDC

def test_motor_derecho():
    configuracion=Logger.load_config("config/motor_config.json")
    motor_derecho= configuracion["motorDerecho"]
    #motor_izquierdo= configuracion["motorIzquierdo"]
    
    try:
        print("Probando motor derecho")
        print("Hacia adelante")
        motor_derecho.set_speed(50)
        time.sleep(2)

        print("Hacia atrás")
        motor_derecho.set_speed(-50)
        time.sleep(2)

        print("Parada")
        motor_derecho.stop()
        time.sleep(1)

        print("Frenado")

    finally:
        if 'motor_derecho' in locals():
            motor_derecho.cleanup()
        print("Prueba de motor derecho finalizada.")


    