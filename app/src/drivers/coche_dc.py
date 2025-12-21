class Coche:
    def __init__(self, motor_izquierdo, motor_derecho, sensor_ultrasonido):
        self.motor_izquierdo = motor_izquierdo
        self.motor_derecho = motor_derecho
        self.sensor_ultrasonido = sensor_ultrasonido

    def avanzar(self, velocidad):
        self.motor_izquierdo.set_speed(velocidad)
        self.motor_derecho.set_speed(velocidad)
    
    def retroceder(self, velocidad):
        self.motor_izquierdo.set_speed(-velocidad)
        self.motor_derecho.set_speed(-velocidad)
    
    def girar_eje_izquierda(self, velocidad):
        self.motor_izquierdo.set_speed(-velocidad)
        self.motor_derecho.set_speed(velocidad)
    
    def girar_eje_derecha(self, velocidad):
        self.motor_izquierdo.set_speed(velocidad)
        self.motor_derecho.set_speed(-velocidad)

    def girar_izquierda(self, velocidad):
        self.motor_izquierdo.set_speed(0)
        self.motor_derecho.set_speed(velocidad)  
    
    def girar_derecha(self, velocidad):
        self.motor_izquierdo.set_speed(velocidad)
        self.motor_derecho.set_speed(0)

    def detener(self):
        self.motor_izquierdo.set_speed(0)
        self.motor_derecho.set_speed(0)

    def medir_distancia(self):
        return self.sensor_ultrasonido.medir_distancia()