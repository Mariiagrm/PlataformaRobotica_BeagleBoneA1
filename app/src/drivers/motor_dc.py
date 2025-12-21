from hal.gpio_sys import GpioSysfs as GPIO
from  hal.pwm_sys import PwmSysfs as PWM

class Motor:
    def __init__(self, pin_pwm, pin_dirA, pin_dirB, pin_encoder, frequency=1000):
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
        self.periodo = 1000/frequency  # Periodo en ms
        self.gpioPWM=PWM(pin_pwm,self.periodo, 0, 1)

        self.pin_encoder=GPIO(pin_encoder, "in")
        print(f"Motor inicializado en pines PWM:{pin_pwm}, IN1:{pin_dirA}, IN2:{pin_dirB}, ENC:{pin_encoder}")
    
    def set_speed(self, speed):
        """
        Establece la velocidad y dirección del motor.
        :param speed: Valor entre -100 (máximo reversa) y 100 (máximo adelante).
        """
        # Limitar el valor de speed entre -100 y 100
        #speed = max(min(speed, 100), -100)

        if speed > 0:
            # Movimiento hacia adelante
            self.gpio_dirA.write(1)
            self.gpio_dirB.write(0)
            duty_cycle=speed
        elif speed < 0:
            # Movimiento hacia atrás
            self.gpio_dirA.write(0)
            self.gpio_dirB.write(1)
            duty_cycle=abs(speed)  # El ciclo de trabajo siempre es positivo
        else:
            self.stop()
            return
 

        # Aplicar el ciclo de trabajo al PWM
        self.gpioPWM.set_duty_cycle(duty_cycle)

        print(f"Velocidad del motor establecida a {speed} (Duty Cycle: {duty_cycle}%)")

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
        
