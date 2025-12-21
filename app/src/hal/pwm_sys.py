import os
import time

class PwmSysfs:
    def __init__(self, pin_name, period=20000, duty_cycle=0, enable=1):
        # Mapeo básico de nombres comunes a números GPIO internos de la BeagleBone
        # Puedes añadir más aquí buscando "BeagleBone P9_XX pwm number"
        self.mapping = {
            "P9_14": "pwm-2:0", "P9_16": "pwm-2:1"
        }
        
        if pin_name not in self.mapping:
            raise ValueError(f"Pin {pin_name} no mapeado en la clase PwmSysfs")
            
        self.pwm_num = self.mapping[pin_name]
        self.path = f"/sys/class/pwm/{self.pwm_num}"
        

        # 2. Configurar parametros PWM
        # Deshabilitar PWM antes de cambiar el periodo
       # 3. SECUENCIA DE INICIALIZACIÓN "ANTI-ERROR"
        # Para evitar "Invalid Argument", el orden debe ser estricto:
        
        # A) Deshabilitar primero
        self.set_enable(0)

        # B) Poner Duty Cycle a 0. 
        # CRÍTICO: Si el Duty actual es > que el nuevo Periodo, el kernel rechaza el cambio de periodo.
        self.set_duty_cycle(0)

        # C) Ahora es seguro cambiar el Periodo
        self.set_period(period)

        # D) Establecer el Duty Cycle deseado
        self.set_duty_cycle(duty_cycle)

        # E) Habilitar finalmente
        self.set_enable("1")
        print(f"PWM {pin_name} iniciado correctamente.")
        print("Path:", f"{self.path}")
        

    def set_period(self, period_ns):
        try:
            with open(f"{self.path}/period", "w") as f:
                f.write(str(int(period_ns)))
        except OSError as e:
            print(f"Error escribiendo Periodo: {e}")
           

    def set_duty_cycle(self, duty_ns):
        try:
            with open(f"{self.path}/duty_cycle", "w") as f:
                f.write(str(int(duty_ns)))
        except OSError as e:
            print(f"Error escribiendo Duty: {e} (Recuerda: Duty no puede ser mayor que Period)")

    def set_enable(self, enable):
        try:
            with open(f"{self.path}/enable", "w") as f:
                f.write(str(enable))
        except OSError as e:
            print(f"Error cambiando Enable: {e}")

    def cleanup(self):
        self.set_enable("0")
        # Opcional: Des-exportar (liberar el pin para otros programas)
        try:
            with open(f"{self.chip_path}/unexport", "w") as f:
                f.write(self.channel)
        except:
            pass