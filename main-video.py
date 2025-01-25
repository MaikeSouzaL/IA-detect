from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import uvicorn
import torch
from ultralytics import YOLO
import cv2

# Inicializar o aplicativo FastAPI
app = FastAPI()

# Verifique se a GPU está disponível
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Carregar o modelo treinado
modelo = YOLO('best.pt').to(device)

@app.get("/processar-camera/")
async def processar_camera(url: str = Query(..., description="URL do stream da câmera IP")):
    """
    Processar a câmera IP em tempo real e retornar os frames anotados.
    """
    # Iniciar captura do stream da câmera
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        return {"erro": "Não foi possível conectar à câmera IP. Verifique o URL."}

    def gerar_frames():
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Realizar a previsão com ajustes de confiança e IoU
            resultados = modelo.predict(frame, conf=0.5, iou=0.4, verbose=False, device=device)[0]

            # Processar as detecções
            for item in resultados.boxes:
                classe = int(item.cls)
                nome_classe = resultados.names[classe]
                x1, y1, x2, y2 = map(int, item.xyxy[0])
                conf = float(item.conf[0]) * 100  

                # Desenhar as caixas de detecção
                cor_caixa = (0, 255, 0) if nome_classe == "pneu" else (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), cor_caixa, 2)
                texto = f"{nome_classe} ({conf:.2f}%)"
                cv2.putText(frame, texto, (x1, max(0, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor_caixa, 2, cv2.LINE_AA)

            # Codificar o frame em JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    # Fechar a captura quando terminar
    cap.release()

    # Retornar o stream como resposta
    return StreamingResponse(gerar_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089)
