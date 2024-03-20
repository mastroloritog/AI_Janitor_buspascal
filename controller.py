import cv2

class CentralModule:
    def __init__(self, robot):
        self.robot = robot
        self.oggetti_riconosciuti = []
        # Inizializza la webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
    
    def start(self):
        while True:
            success, img = self.cap.read()
            if success:
                # Previsioni del modello
                pred = self.robot.recognize_realtime(img)
                # Pulisci l'array degli oggetti riconosciuti
                self.oggetti_riconosciuti.clear()

                # Se riconosce qualcosa
                if pred is not None and len(pred) > 0:
                    # Salva tutti gli oggetti riconosciuti nell'array
                    self.oggetti_riconosciuti = pred.tolist()

                    # Estraiamo solo il primo elemento dalla lista di oggetti riconosciuti, in modo da raccogliere la spazzatura in modo sequenziale
                    primo_oggetto = pred[0]

                    # Estraiamo la classe dell'oggetto
                    classe_oggetto = int(primo_oggetto[5])  # L'indice 5 rappresenta la classe dell'oggetto nella previsione
                    # Determiniamo cosa fare in base alla classe dell'oggetto

                    if classe_oggetto == 0:# Funzione per raggiungere la spazzatura

                        # Coordinate nello schermo dell'oggetto identificato
                        x1, y1, x2, y2 = map(int, primo_oggetto[:4])

                        # Disegno del rettangolo intorno all'oggetto
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                        # Visualizzazione del label sulla camera
                        label = "Collectable Junk"
                        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        
                        self.robot.activate_target_movement(img, x1, x2, y1, y2)

                    elif classe_oggetto == 1: # Funzione per muovere il braccio 
                        self.robot.activate_arm()
                else:
                    # Funzione per giorovagare randomicamente finché non trova spazzatura, nel caso non riconosca nulla
                    self.robot.activate_random_movement()


                # Visualizzazione dell'immagine
                cv2.imshow('Webcam', img)
                if cv2.waitKey(1) == ord('q'):
                    self.terminate()
                    break
    
    def terminate(self):
        self.robot.close_serial_comunication()
        self.cap.release()
        cv2.destroyAllWindows()