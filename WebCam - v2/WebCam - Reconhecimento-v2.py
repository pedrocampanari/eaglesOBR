import serial
import cv2
import numpy as np

text = ""
webcam = cv2.VideoCapture(3)
webcam1 = cv2.VideoCapture(0)
arduino = serial.Serial('/dev/ttyUSB0', 9600)

if (webcam.isOpened()) and (arduino.isOpen()):
    print("Cam conect sucessuful - 1!!")
    print("Serial conect sucessuful!!")
    if webcam1.isOpened():
       print("Cam conect sucessuful - 2!!")
    
    while True:
      
        _, frames = webcam.read()
        _, frames1 = webcam1.read()
        offset = 200
        a,l,_ = frames.shape
        
        #                  V            H      
        campo1 = frames[50:360, offset:l-offset]
        campo2 = frames[50:285, 150:180]
        campo3 = frames[50:285, 460:490]
        campo4 = frames[0:20, 320-40:320+40]
        campo5 = frames[30:250, 0:35]
        campo6 = frames[30:250, 605:640]
        cv2.rectangle(frames,(offset,50), (l-offset,360), (255,120,0), 2)
        cv2.rectangle(frames,(150,50), (180,285), (255,120,0), 2)
        cv2.rectangle(frames,(460,50), (490,285), (255,120,0), 2)
        cv2.rectangle(frames,(320-40,0), (320+40,20), (255,120,0), 2)
        cv2.rectangle(frames,(0,30), (35,250), (255,120,0), 2)
        cv2.rectangle(frames,(605,30), (640,250), (255,120,0), 2)

        media1 = np.average(campo1, axis=0)
        mediac1 = np.average(media1, axis=0)

        media2 = np.average(campo2, axis=0)
        mediac2 = np.average(media2, axis=0)

        media3 = np.average(campo3, axis=0)
        mediac3 = np.average(media3, axis=0)
        
        media4 = np.average(campo4, axis=0)
        mediac4 = np.average(media4, axis=0)

        media5 = np.average(campo5, axis=0)
        mediac5 = np.average(media5, axis=0)

        media6 = np.average(campo6, axis=0)
        mediac6 = np.average(media6, axis=0)

        r1,g1,b1 = int(mediac1[2]), int(mediac1[1]), int(mediac1[0])
        r2,g2,b2 = int(mediac2[2]), int(mediac2[1]), int(mediac2[0])
        r3,g3,b3 = int(mediac3[2]), int(mediac3[1]), int(mediac3[0])
        r4,g4,b4 = int(mediac4[2]), int(mediac4[1]), int(mediac4[0])
        r5,g5,b5 = int(mediac5[2]), int(mediac5[1]), int(mediac5[0])
        r6,g6,b6 = int(mediac6[2]), int(mediac6[1]), int(mediac6[0])

        cv2.putText(frames, "R:{} G:{} B:{}".format(r1, g1, b1), (250, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (120,255,0), 1, cv2.LINE_AA)
        cv2.putText(frames, "R:{} G:{} B:{}".format(r2, g2, b2), (30, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120,255,0), 1, cv2.LINE_AA)
        cv2.putText(frames, "R:{} G:{} B:{}".format(r3, g3, b3), (460, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120,255,0), 1, cv2.LINE_AA)
        cv2.putText(frames, "R:{} G:{} B:{}".format(r4, g4, b4), (250, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120,255,0), 1, cv2.LINE_AA)
        cv2.putText(frames, "{}".format(text), (180, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2, cv2.LINE_AA)
        cv2.putText(frames, "R:{} G:{} B:{}".format(r5, g5, b5), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120,255,0), 1, cv2.LINE_AA)
        cv2.putText(frames, "R:{} G:{} B:{}".format(r6, g6, b6), (485, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120,255,0), 1, cv2.LINE_AA)

        if (r1 <= 125 and g1 <= 130 and b1 <= 140):
            if (r2 >= 160 and g2 >= 165 and b2 >= 190) and (r3 >= 175 and g3 >= 165 and b3 >= 190):
               text = "Linha preta - Siga em Frente"
               arduino.write(b'1')
            elif ((r5 <= 145 and g5 <= 165 and b5 <= 180) or (r6 <= 145 and g6 <= 165 and b6 <= 180)) and (r4 < 190 and g4 < 210 and b4 < 240):
               text = "Desvio detectado - Seguir reto"
               arduino.write(b'2')
            elif (r5 <= 50 and g5 <= 40 and b5 <= 40) and (r4 >= 190 and g4 >= 200 and b4 >= 220):
               text = "Desvio detectado - Curva 90 Esquerda"
               arduino.write(b'3')
            elif (r6 <= 50 and g6 <= 40 and b6 <= 40) and (r4 >= 190 and g4 >= 200 and b4 >= 220):
               text = "Desvio detectado - Curva 90 Direita"
               arduino.write(b'4')
            elif r2  < 210 and g2 < 180 and b2 < 190:
               text = "Rota desvida - Correcao Direita"
               arduino.write(b'6')
            elif r3  < 210 and g3 < 180 and b3 < 190:
               text = "Rota desvida - Correcao Esquerda"
               arduino.write(b'5')
        else:
            text = "Rota Perdida!"
            arduino.write(b'7')
        
        cv2.imshow("Video WEBCAM - Index", frames)
        cv2.imshow("Video WEBCAM - Index 2", frames1)
        #cv2.imshow("Teste", campo1)
        #cv2.imshow("Teste -1", campo2)
        #cv2.imshow("Teste -2", campo3)
        #cv2.imshow("Teste -3", campo4)
        #cv2.imshow("Teste -4", campo5)
        #cv2.imshow("Teste -5", campo6)
        key = cv2.waitKey(5)
        if key == 27:
            break

arduino.close()
cv2.release()
cv2.destroyAllWindows()
