from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import uvicorn
import torch
from ultralytics import YOLO
import cv2
import numpy as np
import os

# Inicializar o aplicativo FastAPI
app = FastAPI()

# Verifique se a GPU está disponível
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Carregar o modelo treinado
modelo = YOLO('best.pt').to(device)

# Pasta para salvar a imagem processada
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)


@app.post("/processar-imagem/")
async def processar_imagem(file: UploadFile = File(...)):
    # Salvar a imagem recebida
    input_path = os.path.join(output_dir, file.filename)
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Carregar a imagem
    imagem = cv2.imread(input_path)

    if imagem is None:
        return {"erro": f"Erro ao carregar a imagem '{file.filename}'."}

    # Realizar a previsão com ajustes de confiança e IoU
    resultados = modelo.predict(imagem, conf=0.5, iou=0.4, verbose=False, device=device)[0]

    # Inicializar variáveis
    maior_veiculo = None
    maior_area = 0
    veiculo_nome = ""
    veiculo_coordenadas = None

    # Processar as detecções para encontrar o maior veículo
    for item in resultados.boxes:
        classe = int(item.cls)
        nome_classe = resultados.names[classe]

        if nome_classe in ["carro", "moto", "truck"]:  # Classes de veículos
            x1, y1, x2, y2 = map(int, item.xyxy[0])
            area = (x2 - x1) * (y2 - y1)

            if area > maior_area:
                maior_area = area
                maior_veiculo = nome_classe
                veiculo_coordenadas = (x1, y1, x2, y2)

    # Verificar se algum veículo foi detectado
    if not maior_veiculo or not veiculo_coordenadas:
        return {"erro": "Nenhum veículo detectado na imagem."}

    # Inicializar contadores
    total_eixos_normais = 0
    total_eixos_erguidos = 0
    total_rodas = 0

    x1_v, y1_v, x2_v, y2_v = veiculo_coordenadas

    # Processar novamente para contar e desenhar os detalhes dentro do maior veículo
    for item in resultados.boxes:
        classe = int(item.cls)
        nome_classe = resultados.names[classe]
        x1, y1, x2, y2 = map(int, item.xyxy[0])

        # Verificar se a detecção está dentro da área do maior veículo
        if x1_v <= x1 <= x2_v and y1_v <= y1 <= y2_v:
            if nome_classe == "pneu":
                total_eixos_normais += 1
                total_rodas += 2
                cor_caixa = (0, 255, 0)  # Verde para pneus
            elif nome_classe == "eixo_suspenso":
                total_eixos_erguidos += 1
                total_eixos_normais += 1
                total_rodas += 2
                cor_caixa = (0, 0, 255)  # Vermelho para eixo suspenso
            else:
                cor_caixa = (255, 255, 0)  # Amarelo para outras classes

            # Desenhar a caixa do objeto
            cv2.rectangle(imagem, (x1, y1), (x2, y2), cor_caixa, 2)
            cv2.putText(imagem, nome_classe, (x1, max(0, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor_caixa, 2, cv2.LINE_AA)

    # Desenhar a caixa do maior veículo
    cv2.rectangle(imagem, (x1_v, y1_v), (x2_v, y2_v), (255, 0, 0), 3)  # Azul para o veículo selecionado
    texto_veiculo = f"{maior_veiculo}: {total_eixos_normais} eixos, {total_eixos_erguidos} erguidos, {total_rodas} rodas"
    cv2.putText(imagem, texto_veiculo, (x1_v, y1_v - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2, cv2.LINE_AA)

    # Salvar a imagem processada
    output_path = os.path.join(output_dir, f"resultado_{file.filename}")
    cv2.imwrite(output_path, imagem)

    # Retornar a imagem processada
    return FileResponse(output_path, media_type="image/jpeg", filename=f"resultado_{file.filename}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8189)