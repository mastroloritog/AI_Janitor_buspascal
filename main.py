from controller import CentralModule
from robot_model import Robot

# inserire porta arduino e percorso modello yolov5 corretti
robot = Robot("COMx", 9600, "Path/to/best.pt")
central_module = CentralModule(robot)

central_module.start()
