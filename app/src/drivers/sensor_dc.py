import time
from hal.gpio_sys import GpioSysfs as GPIO

class Sensor:
    def __init__(self, pin_echo, pin_trigger):
        # Asumiendo que tu clase GPIO funciona bien
        self.gpio_echo = GPIO(pin_echo, "in")
        self.gpio_trigger = GPIO(pin_trigger, "out")
        self.gpio_trigger.write(0)
        
        print(f"Sensor inicializado. TRIG:{pin_trigger}, ECHO:{pin_echo}")

    def medir_distancia(self):
        import time
        
        # 1. TRIGGER
        self.gpio_trigger.write(1)
        time.sleep(0.000015) # Un pelín más de 10us por seguridad
        self.gpio_trigger.write(0)

        # 2. ESPERAR INICIO (LOW -> HIGH)
        timeout_start = time.time()
        while self.gpio_echo.read() == 0:
            # Timeout corto (si no empieza en 0.1s, error)
            if time.time() - timeout_start > 0.1:
                # Retornamos None para diferenciar de error de rango
                print("Error: El sensor no responde (Check VCC/GND)")
                return None 
        
        # Marcamos el inicio AHORA MISMO
        start_time = time.time()

        # 3. ESPERAR FIN (HIGH -> LOW)
        while self.gpio_echo.read() == 1:
            # Timeout largo: Aceptamos hasta 100ms (aprox 17 metros teóricos)
            # Esto cubre el caso de "Sensor no ve nada" (pulso de 38ms + lag de Python)
            if time.time() - start_time > 0.1:
                print("Aviso: Objeto fuera de rango o señal perdida")
                return -1 
        
        stop_time = time.time()

        # 4. CÁLCULO
        elapsed_time = stop_time - start_time
        
        # Corrección por latencia de SysFS (Python es lento leyendo archivos)
        # SysFS tarda ~0.001s en leer. Restamos un poco para compensar el lag.
        # Ajusta este valor "calibracion" si ves que mide siempre de más.
        calibracion = 0.0005 
        elapsed_time = max(0, elapsed_time - calibracion)

        distance = (elapsed_time * 34300) / 2 
        return distance