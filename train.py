from ultralytics import YOLO

# Testar o carregamento do arquivo de configuração
data_config = "data.yaml"
try:
    model = YOLO("yolov8x.pt")
    model.train(data=data_config, epochs=1, imgsz=640)  # Apenas 1 época para validar
    print("Configuração verificada com sucesso!")
except Exception as e:
    print(f"Erro ao verificar o arquivo data.yaml: {e}")