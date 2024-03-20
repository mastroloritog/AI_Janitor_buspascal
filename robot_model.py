import numpy as np
import torch
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression
import serial
import time

class Robot:
    def __init__(self, comPort, baudRate, modelPath):  # comPort: 'COM7', baudRate: 9600, modelPath: "C:/Users/Accappi/Desktop/progetti/PJ/prova1/yolov5/runs/train/junkRecognition_model2/weights/best.pt"
        # Configura la porta seriale
        # cercare comando per trovare su che porta COM è collegato l'arduino
        self.serial_port = serial.Serial(comPort, baudRate, timeout=1)  # Assicurati di sostituire 'COMX' con la porta corretta
        # Aspetta un secondo per stabilire la connessione
        time.sleep(1)
        # Imposta il percorso assoluto del modello best.pt
        self.model_path = modelPath  # percorso assoluto
        # Caricamento del modello YOLOv5 allenato
        # Dispositivo CUDA se disponibile, altrimenti passa al dispositivo CPU
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = attempt_load(self.model_path, device=self.device).to(self.device).eval()
        pass

    def activate_arm(self):
        # codice per gestire il braccio del robot
        pass

    def activate_target_movement(self, img, x1, x2, y1, y2):
        # codice per far muovere il robot verso la spazzatura

        # Calcolo della distanza approssimativa
        object_height = y2 - y1  # Altezza dell'oggetto nell'immagine
        # Calcoliamo il centro dell'oggetto
        x_center = (x1 + x2) // 2
        # Dividiamo la larghezza dell'immagine in tre parti
        image_width = img.shape[1]
        third_width = image_width // 3
        # Determiniamo se l'oggetto si trova nella parte sinistra, destra o centrale
        if x_center < third_width:
            position = "sx"
        elif x_center > 2 * third_width:
            position = "dx"
        else:
            position = "ok"
        print("Posizione nello schermo dell'oggetto riconosciuto:", position)

        # Invia la posizione del primo oggetto ad Arduino tramite comunicazione seriale
        self.serial_port.write(position.encode('utf-8') + b'\n')
        # Leggi la risposta da Arduino
        response = self.serial_port.readline().decode().strip()
        print("Risposta da Arduino:", response)
        return

    def activate_random_movement(self):
        # codice per far muovere il robot in modo casuale
        pass

    def recognize_realtime(self, img):
        # Previsioni del modello
        img_tensor = torch.from_numpy(img).to(self.device)
        img_tensor = img_tensor.permute(2, 0, 1).float().div(255.0).unsqueeze(0)
        pred = self.model(img_tensor)[0]

        # Applica il non-maximum suppression
        pred = non_max_suppression(pred, 0.4, 0.5)[0]

        return pred
    
    def close_serial_comunication(self):
        self.serial_port.close()  # chiusura comunicazione seriale
        return

    # --------------------------------------------------------------------------------------------------------------------------------
    
    

# robot = Robot("COM7", 9600, "C:/Users/Accappi/Desktop/progetti/PJ/prova1/yolov5/runs/train/junkRecognition_model2/weights/best.pt")
