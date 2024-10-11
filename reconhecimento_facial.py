import cv2
import face_recognition
import numpy as np
import pickle
import os

# Função para reconhecer e capturar dados faciais
def reconhecimento_facial():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível acessar a webcam.")
        return None

    print("Capturando rosto... Pressione 'q' para sair.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro: Não foi possível capturar o frame.")
            break

        face_locations = face_recognition.face_locations(frame)

        for face_location in face_locations:
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow('Webcam', frame)

        if len(face_locations) > 0:
            encoding = face_recognition.face_encodings(frame, face_locations)
            if encoding:
                print("Rosto reconhecido com sucesso!")
                # Salvar dados do reconhecimento em um arquivo
                with open('dados_face.pkl', 'wb') as f:
                    pickle.dump(encoding[0], f)  # Salva a codificação do rosto
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    reconhecimento_facial()
