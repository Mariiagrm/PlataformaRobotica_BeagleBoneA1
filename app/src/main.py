import time
#form src.subsystem import DriveTrain
from src.utils.logger import Logger

def main():

    load_config = Logger.load_config("config/settings.json")
    configuracion= Logger.load_config("config/settings.yaml")
#     robot=DriveTrain(configuracion)
#     state= "INITIALIZING"

#     try:
#         while True:
#             if state=="INITIALIZING":
#                 robot.initialize()
#                 state="ESPERA"
#                 sensors=robot.read_sensors()

#             if state=="ESPERA":
#                 if sensors["start_button"]:
#                     state="DRIVING"
#                 elif state=="DRIVING":
#                     robot.move_to()
#                     if sensors["obstacle_detected"]:
#                         state="OBSTACLE_AVOIDANCE"
#                 elif state=="OBSTACLE_AVOIDANCE":
#                     robot.avoid_obstacle()
#                     if not sensors["obstacle_detected"]:
#                         state="DRIVING"
#                     else:
#                         state="PAUSED"
#                 elif state=="PAUSED":
#                     if sensors["stop_button"]:
#                         state="ESPERA"

#             time.sleep(0.1)  # Pequeña pausa para evitar uso excesivo de CPU
#     except KeyboardInterrupt:
#         print("Shutting down robot...")
#         robot.shutdown()

# if __name__ == "__main__":
#     main()
