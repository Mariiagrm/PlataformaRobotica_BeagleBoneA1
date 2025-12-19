import Adafruit_NIO.PWM as PWM
import Adafruit_NIO.GPIO as GPIO

class Motor:
    def __init__(self, pwm_pin, in1_pin, in2_pin, frequency=1000):
        """
        Inicializa el motor DC con control de velocidad y dirección.
        :param pwm_pin: Pin PWM para control de velocidad.
        :param in1_pin: Pin digital para dirección 1.
        :param in2_pin: Pin digital para dirección 2.
        :param frequency: Frecuencia del PWM en Hz.
        """
        self.pwm_pin = pwm_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

        # Configuración de pines como salida
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)

        # Inicializar el motor en estado de parada
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)

        # Configuración del PWM
        PWM.start(self.pwm_pin, 0, frequency)

        print(f"Motor inicializado en pines PWM:{pwm_pin}, IN1:{in1_pin}, IN2:{in2_pin}")
    
    def set_speed(self, speed):
        """
        Establece la velocidad y dirección del motor.
        :param speed: Valor entre -100 (máximo reversa) y 100 (máximo adelante).
        """
        # Limitar el valor de speed entre -100 y 100
        speed = max(min(speed, 100), -100)

        if speed > 0:
            # Movimiento hacia adelante
            GPIO.output(self.in1_pin, GPIO.HIGH)
            GPIO.output(self.in2_pin, GPIO.LOW)
            duty_cycle = speed
        elif speed < 0:
            # Movimiento hacia atrás
            GPIO.output(self.in1_pin, GPIO.LOW)
            GPIO.output(self.in2_pin, GPIO.HIGH)
            duty_cycle = abs(speed)  # El ciclo de trabajo siempre es positivo
        else:
            # Parada (Coast)
            GPIO.output(self.in1_pin, GPIO.LOW)
            GPIO.output(self.in2_pin, GPIO.LOW)
            duty_cycle = 0

        # Aplicar el ciclo de trabajo al PWM
        PWM.set_duty_cycle(self.pwm_pin, duty_cycle)

        print(f"Velocidad del motor establecida a {speed} (Duty Cycle: {duty_cycle}%)")

    def stop(self):
        self.set_speed(0)

   
    def cleanup(self):
        """
        Limpia los recursos del motor.
        """
        self.stop()
        PWM.stop(self.pwm_pin)
        PWM.cleanup()
        GPIO.cleanup([self.in1_pin, self.in2_pin])
        print("Recursos del motor limpiados.")
        
