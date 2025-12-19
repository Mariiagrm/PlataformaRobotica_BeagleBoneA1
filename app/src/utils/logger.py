import json

from src.drivers.motor_dc import Motor#, Sensor

class Logger:
    @staticmethod
    def load_config(file_path):
        # Carga de configuración desde un archivo JSON´

        configuracion = {}
        with open(file_path, 'r') as f:
            config = json.load(f)
        for value in config.values():
            if "motor" in value:
                if "derecho" in value:
                    m=Motor(value["pwm_pin"], value["in1_pin"], value["in2_pin"], value.get("frequency", 2000))
                    configuracion["motorDerecho"] = m
                elif "izquierdo" in value:
                    m=Motor(value["pwm_pin"], value["in1_pin"], value["in2_pin"], value.get("frequency", 2000))
                    configuracion["motorIzquierdo"] = m
            elif "sensor" in value:
                #Sensor(value["pin"], value.get("type", "digital"))
                configuracion["sensorUltrasonido"] = m


        return configuracion
    


