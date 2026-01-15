from hal.gpio_sys import GpioSysfs as GPIO
from  hal.pwm_sys import PwmSysfs as PWM

class Motor:
    def __init__(self, pin_pwm, pin_dirA, pin_dirB, pin_encoder, frequency=0.25
        """
        Inicializa el motor DC con control de velocidad y dirección.
        :param pin_pwm: Pin PWM para control de velocidad.
        :param pin_dirA: Pin digital para dirección 1.
        :param pin_dirB: Pin digital para dirección 2.
        :param frequency: Frecuencia del PWM en Hz.
        """
        
        # Configuración de pines como salida
        self.gpio_dirA=GPIO(pin_dirA, "out")  # Configura el pin
        self.gpio_dirA.write(0)              # Inicializa en bajo
        self.gpio_dirB=GPIO(pin_dirB, "out")
        self.gpio_dirB.write(0)              # Inicializa en bajo
        self.gpio_encoder=GPIO(pin_encoder, "in")  # Configura el pin del encoder
       # Configuración del PWM
        # Si frequency=0.25 , periodo = 4000
        self.periodo = int(1000 / frequency) 
        
        # Inicializamos PWM con periodo calculado, duty 0, habilitado
        self.gpioPWM = PWM(pin_pwm, self.periodo, 0, 1)

        self.pin_encoder = pin_encoder # Guardamos referencia (aunque no se usa aquí todavía)
        print(f"Motor inicializado: PWM={pin_pwm}, DIR={pin_dirA}/{pin_dirB}")

    def leer_encoder(self):
        """
        Lee el valor actual del encoder.
        :return: Valor del encoder (0 o 1).
        """
        return self.gpio_encoder.read()
    
    
    def set_speed(self, speed):
        """
        Establece la velocidad usando una escala 0-100%.
        Mapeo: 60% -> valor PWM 2000.
        """
        # 1. Limitar entrada entre -100 y 100
        speed = max(min(speed, 100), -100)

        # 2. Dirección
        if speed > 0:
            self.gpio_dirA.write(1)
            self.gpio_dirB.write(0)
        elif speed < 0:
            self.gpio_dirA.write(0)
            self.gpio_dirB.write(1)
        else:
            self.stop()
            return

        # 3. Conversión de Escala (La parte que pediste)
        # Si 60% debe ser 2000, entonces el factor es 2000/60 = 33.3333
        pwm_value = int(abs(speed) * (2000 / 60))

        # Seguridad: Nunca exceder el periodo (4000)
        if pwm_value >= self.periodo:
            pwm_value = self.periodo - 10

        self.gpioPWM.set_duty_cycle(pwm_value)
        # print(f"Velocidad: {speed}% -> PWM: {pwm_value}/{self.periodo}")


    def stop(self):
        self.gpioPWM.set_duty_cycle(0)
        self.gpio_dirA.write(0)
        self.gpio_dirB.write(0)
        

   
    def cleanup(self):
        """
        Limpia los recursos del motor.
        """
        self.stop()
        self.gpioPWM.cleanup()
        self.gpio_dirA.cleanup()
        self.gpio_dirB.cleanup()
        print("Recursos del motor limpiados.")
        
