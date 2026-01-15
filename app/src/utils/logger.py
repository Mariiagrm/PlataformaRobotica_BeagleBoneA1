import json

from drivers.motor_dc import Motor
from drivers.sensor_dc import Sensor
from drivers.coche_dc import Coche

class Logger:
    @staticmethod
    def load_config(file_path):
        # Carga de configuración desde un archivo JSON´

        configuracion = {}
        try: 
            with open(file_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error al cargar el archivo de configuración: {e}")
            newfile_path="src/config/settings.json"
            with open(newfile_path, 'r') as f:
                config = json.load(f)
              

    
        for key, value in config.items():
            if "motor" in key:
                if "derecho" in key:
                    m=Motor(value["pin_pwm"], value["pin_dirA"], value["pin_dirB"], value["pin_encoder"], value.get("frequency", 2000))
                    configuracion["motor_derecho"] = m
                elif "izquierdo" in key:
                    m=Motor(value["pin_pwm"], value["pin_dirA"], value["pin_dirB"], value["pin_encoder"], value.get("frequency", 2000))
                    configuracion["motor_izquierdo"] = m
            elif "sensor" in key:
                sensor=Sensor(value["pin_echo"], value["pin_trigger"])
                configuracion["sensor_ultrasonido"] = sensor

        coche = Coche(configuracion["motor_izquierdo"], configuracion["motor_derecho"], configuracion["sensor_ultrasonido"])
        return coche
    
    def load_config_parts(file_path, pieza = None):
        """Devuelve el objeto correspondiente a la pieza solicitada.
        para pieza: 'motor_derecho', 'motor_izquierdo', 'sensor_ultrasonido'"""
        # Carga de configuración desde un archivo JSON´

        configuracion = {}
        try: 
            with open(file_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error al cargar el archivo de configuración: {e}")
            newfile_path="src/config/settings.json"
            with open(newfile_path, 'r') as f:
                config = json.load(f)
              

    
        for key, value in config.items():
            if "motor" in key and (pieza is None or pieza in key):
                if "derecho" in key:
                    m=Motor(value["pin_pwm"], value["pin_dirA"], value["pin_dirB"], value["pin_encoder"], value.get("frequency", 2000))
                    return m
                elif "izquierdo" in key and (pieza is None or pieza in key):
                    m=Motor(value["pin_pwm"], value["pin_dirA"], value["pin_dirB"], value["pin_encoder"], value.get("frequency", 2000))
                    return m

            elif "sensor" in key and (pieza is None or pieza in key):
                sensor=Sensor(value["pin_echo"], value["pin_trigger"])
                configuracion["sensor_ultrasonido"] = sensor
                return sensor

        
    


