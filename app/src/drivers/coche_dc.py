class Coche:
    def __init__(self, motor_izquierdo, motor_derecho, sensor_ultrasonido):
        self.motor_izquierdo = motor_izquierdo
        self.motor_derecho = motor_derecho
        self.sensor_ultrasonido = sensor_ultrasonido

    def leer_sensores(self):
        distancia = self.sensor_ultrasonido.medir_distancia()
        return distancia
    
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
    
    def girar_izquierda_endoder(self, velocidad):
        """Gira a la izquierda girando motor derecho tras 32 pulsos del encoder."""
        self.motor_derecho.leer_encoder() # devuelve 0 o 1
        pulsos = 0
        while pulsos < 32:
            self.motor_derecho.set_speed(velocidad)
            if self.motor_derecho.leer_encoder() == 1:
                pulsos += 1
                while self.motor_derecho.leer_encoder() == 1:
                    pass  # Espera a que baje a 0
        self.motor_derecho.set_speed(0)

    def girar_derecha_endoder(self, velocidad):
        """Gira a la derecha girando motor derecho tras 32 pulsos del encoder."""
        self.motor_izquierdo.leer_encoder() # devuelve 0 o 1
        pulsos = 0
        while pulsos < 32:
            self.motor_derecho.set_speed(velocidad)
            if self.motor_izquierdo.leer_encoder() == 1:
                pulsos += 1
                while self.motor_izquierdo.leer_encoder() == 1:
                    pass  # Espera a que baje a 0
        self.motor_izquierdo.set_speed(0)
    

    def detener(self):
        self.motor_izquierdo.set_speed(0)
        self.motor_derecho.set_speed(0)

    def medir_distancia(self):
        return self.sensor_ultrasonido.medir_distancia()