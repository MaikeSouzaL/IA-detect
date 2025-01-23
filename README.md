# 🚗 IA DETECT - Sistema de Detecção Veicular

Sistema de detecção e classificação de veículos usando YOLOv8 e FastAPI.

## 🎯 Funcionalidades

- Detecção de veículos (carros, motos, caminhões)
- Contagem automática de eixos e rodas
- API REST para processamento de imagens
- Interface web para visualização
- Suporte a processamento em tempo real
- Captura de frames de vídeo

## ⚙️ Requisitos

- Python 3.10.1
- CUDA compatível (opcional, para GPU)
- 4GB RAM mínimo
- 500MB espaço em disco

## 🚀 Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ia-detect.git
cd ia-detect

# Crie e ative o ambiente virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

# Instale as dependências
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto

```
ia-detect/
├── imgBase/       # Imagens/vídeos de entrada
├── output/        # Resultados processados
├── dataset/       # Dados de treinamento
│   ├── train/
│   ├── test/
│   └── val/
├── main.py        # API FastAPI
├── show.py        # Interface de captura
├── split.py       # Divisão de dataset
├── train.py       # Treinamento do modelo
└── data.yaml      # Configuração YOLO
```

## 💻 Como Usar

1. **Captura de Imagens**
```bash
python show.py
```
- Tecla `1`: Processar imagem
- Tecla `2`: Processar vídeo
  - `Espaço`: Pausar/Continuar
  - `S`: Capturar frame
  - `Q`: Sair

2. **API de Detecção**
```bash
python main.py
```
- Acesse: http://localhost:8189/docs
- Endpoint: POST /processar-imagem/

3. **Treinar Modelo**
```bash
python train.py
```

## 📊 Configuração do Modelo

1. Configure `data.yaml`:
```yaml
path: ./dataset
train: train/images
val: val/images
test: test/images
nc: 4  # classes
names: ['carro', 'moto', 'truck', 'pneu']
```

2. Coloque `best.pt` na raiz do projeto

## 📝 Resultados

O sistema gera:
- Detecção de veículos com bounding boxes
- Contagem de eixos e rodas
- Classificação do tipo de veículo
- Imagens processadas em `/output`

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

Link do Projeto: [https://github.com/seu-usuario/ia-detect](https://github.com/seu-usuario/ia-detect)
