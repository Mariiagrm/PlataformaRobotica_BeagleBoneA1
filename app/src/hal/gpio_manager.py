import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

class MotorDC:
    def __init__(self, pwm_pin, in1_pin, in2_pin, frequency=2000):
        """
        Inicializa un motor DC.
        :param pwm_pin: Pin conectado a la entrada PWM del driver (ej. "P9_14")
        :param in1_pin: Pin de dirección 1 (ej. "P9_12")
        :param in2_pin: Pin de dirección 2 (ej. "P9_15")
        :param frequency: Frecuencia del PWM en Hz (default 2kHz para evitar ruido audible)
        """
        self.pwm_pin = pwm_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

        # Configuración de GPIOs de Dirección
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)
        
        # Inicializamos en STOP
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)

        # Configuración del PWM
        # PWM.start(channel, duty_cycle, frequency, polarity)
        PWM.start(self.pwm_pin, 0, frequency)
        
        print(f"Motor inicializado en pines PWM:{pwm_pin}, IN1:{in1_pin}, IN2:{in2_pin}")

    def set_speed(self, speed):
        """
        Controla la velocidad y dirección del motor.
        :param speed: Valor entre -100 (máx reversa) y 100 (máx adelante).
        """
        # 1. Limitar el valor entre -100 y 100 (Clamping)
        speed = max(min(speed, 100), -100)

        # 2. Lógica de Dirección
        if speed > 0:
            # Adelante
            GPIO.output(self.in1_pin, GPIO.HIGH)
            GPIO.output(self.in2_pin, GPIO.LOW)
            duty_cycle = speed
            
        elif speed < 0:
            # Atrás
            GPIO.output(self.in1_pin, GPIO.LOW)
            GPIO.output(self.in2_pin, GPIO.HIGH)
            duty_cycle = abs(speed) # El PWM siempre es positivo
            
        else:
            # Parada (Coast)
            GPIO.output(self.in1_pin, GPIO.LOW)
            GPIO.output(self.in2_pin, GPIO.LOW)
            duty_cycle = 0

        # 3. Aplicar al hardware
        PWM.set_duty_cycle(self.pwm_pin, duty_cycle)

    def brake(self):
        """Frenado fuerte (cortocircuito de bobinas en Puente H)"""
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.HIGH)
        PWM.set_duty_cycle(self.pwm_pin, 100)

    def cleanup(self):
        """Apaga el motor y libera recursos. Crítico para seguridad."""
        PWM.stop(self.pwm_pin)
        PWM.cleanup()
        GPIO.cleanup()