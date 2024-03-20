from controller import CentralModule
from robot_model import Robot

# inserire porta arduino e percorso modello yolov5 corretti
robot = Robot("COM7", 9600, "C:/Users/Accappi/Desktop/progetti/PJ/prova1/yolov5/runs/train/junkRecognition_model2/weights/best.pt")
central_module = CentralModule(robot)

central_module.start()