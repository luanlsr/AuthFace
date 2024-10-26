import cv2
import pickle


def capturar_reconhecimento_facial(camera_index=0):  # Mude o índice da câmera se necessário
    # Carregar o classificador Haar Cascade para detecção de rostos
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Abrir a câmera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Erro ao abrir a câmera")
        return None

    rosto_detectado = False
    dados_face = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha na captura de vídeo")
            break

        # Converter o frame para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detectar rostos
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) > 0:
            # Usar apenas o primeiro rosto detectado
            (x, y, w, h) = faces[0]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Desenhar retângulo ao redor do rosto
            dados_face = cv2.resize(gray[y:y + h, x:x + w], (100, 100))  # Redimensionar a imagem facial
            rosto_detectado = True
            print("Rosto detectado, capturando dados faciais.")
        else:
            print("Nenhum rosto detectado.")

        # Exibir a imagem capturada
        cv2.imshow('Reconhecimento Facial', frame)
        cv2.waitKey(1000)  # Delay de 3 segundos
        # Pressione 'q' para sair ou continue se o rosto foi detectado
        if cv2.waitKey(1) & 0xFF == ord('q') or rosto_detectado:
            break

    # Liberar a câmera e fechar todas as janelas
    cap.release()
    cv2.destroyAllWindows()

    # Salvar os dados faciais redimensionados
    if rosto_detectado and dados_face is not None:
        with open('dados_face.pkl', 'wb') as f:
            pickle.dump(dados_face, f)
        print("Rosto capturado e salvo com sucesso!")
        print(dados_face)
        return dados_face
    else:
        print("Nenhum rosto foi detectado.")
        return None


if __name__ == "__main__":
    capturar_reconhecimento_facial(camera_index=0)  # Use o índice correto da câmera
