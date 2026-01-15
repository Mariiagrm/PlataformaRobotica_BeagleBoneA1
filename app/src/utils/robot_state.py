import threading

class RobotState:
    """
    Esta clase actúa como memoria compartida entre el hilo de teclado
    y el hilo del robot.
    """
    def __init__(self):
        self.mode = "STOP"      # Modos: STOP, MANUAL, AUTO
        self.command = "libre"  # Comandos: adelante, atras, derecha, izquierda
        self.speed = 2000         # Velocidad actual (0-100)
        self.distance=0      # Distancia del sensor ultrasónico
        self.running = True     # Para apagar el programa suavemente
        self.lock = threading.Lock() # Semáforo para evitar conflictos de memoria

    def update(self, mode=None, command=None, speed=None, distance=None):
        """Actualiza el estado de forma segura (Thread-Safe)"""
        with self.lock:
            if mode: self.mode = mode
            if command: self.command = command
            if speed is not None: self.speed = int(speed)
            if distance is not None: self.distance = distance

    def get_state(self):
        """Devuelve una copia del estado actual"""
        with self.lock:
            return self.mode, self.command, self.speed, self.distance
