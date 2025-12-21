import os
import time

class GpioSysfs:
    def __init__(self, pin_name, direction="out"):
        # Mapeo básico de nombres comunes a números GPIO internos de la BeagleBone
        # Puedes añadir más aquí buscando "BeagleBone P9_XX gpio number"
        self.mapping = {
            "P9_25": "177",
            "P9_18": "208",
            "P8_07": "165",
            "P8_08": "166",
            "P8_09": "178",
            "P8_10": "164",
            "P8_36": "234", 
            "P9_17": "209"
        }
        
        if pin_name not in self.mapping:
            raise ValueError(f"Pin {pin_name} no mapeado en la clase GpioSysfs")
            
        self.gpio_num = self.mapping[pin_name]
        self.path = f"/sys/class/gpio/gpio{self.gpio_num}"
        
        # 1. Exportar el pin (hacerlo visible) si no lo está
        if not os.path.exists(self.path):
            try:
                with open("/sys/class/gpio/export", "w") as f:
                    f.write(self.gpio_num)
            except OSError:
                print(f"Aviso: El pin {pin_name} ya estaba exportado o ocupado.")

        # Esperar un momento a que el sistema cree los archivos
        time.sleep(0.1)

        # 2. Configurar dirección
        try:
            with open(f"{self.path}/direction", "w") as f:
                f.write(direction)
        except PermissionError:
             print("ERROR DE PERMISOS: Recuerda usar sudo o --privileged en Docker")
        
        print(f"{pin_name} configurada correctamente")
        print("Path:", f"{self.path}")

    
    def write(self, value):
        # Value debe ser 1 o 0
        with open(f"{self.path}/value", "w") as f:
            f.write(str(value))

    def read(self):
        with open(f"{self.path}/value", "r") as f:
            return int(f.read().strip())
        
    def cleanup(self):
        # Opcional: Des-exportar el pin al cerrar
        try:
            with open("/sys/class/gpio/unexport", "w") as f:
                f.write(self.gpio_num)
        except:
            pass