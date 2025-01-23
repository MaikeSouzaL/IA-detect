import os
import shutil
import random

# Caminho da pasta de saída onde estão as imagens capturadas
pasta_output = "output"
pasta_destino = "dataset"  # Pasta base onde serão criadas train, test e val

# Proporções para divisão
proporcao_train = 0.7
proporcao_test = 0.15
proporcao_val = 0.15

# Verificar se a pasta de saída existe
if not os.path.exists(pasta_output):
    print(f"Erro: A pasta '{pasta_output}' não foi encontrada.")
    exit()

# Criar a estrutura de pastas: train, test, val
for subset in ['train', 'test', 'val']:
    subset_path = os.path.join(pasta_destino, subset)
    img_path = os.path.join(subset_path, "img")
    label_path = os.path.join(subset_path, "label")

    # Criar as pastas caso não existam
    os.makedirs(img_path, exist_ok=True)
    os.makedirs(label_path, exist_ok=True)

# Listar todas as imagens na pasta output
imagens = [f for f in os.listdir(pasta_output) if f.endswith(('.jpg', '.png', '.jpeg'))]

# Embaralhar as imagens para garantir uma divisão aleatória
random.shuffle(imagens)

# Dividir as imagens
total_imagens = len(imagens)
num_train = int(total_imagens * proporcao_train)
num_test = int(total_imagens * proporcao_test)

imagens_train = imagens[:num_train]
imagens_test = imagens[num_train:num_train + num_test]
imagens_val = imagens[num_train + num_test:]

# Função para mover as imagens para suas respectivas pastas
def mover_imagens(imagens, destino):
    for imagem in imagens:
        origem = os.path.join(pasta_output, imagem)
        destino_img = os.path.join(destino, "img", imagem)
        shutil.copy(origem, destino_img)  # Copiar a imagem para a subpasta img

# Mover as imagens para as pastas train, test e val
mover_imagens(imagens_train, os.path.join(pasta_destino, "train"))
mover_imagens(imagens_test, os.path.join(pasta_destino, "test"))
mover_imagens(imagens_val, os.path.join(pasta_destino, "val"))

print(f"Divisão concluída com sucesso!")
print(f"Total de imagens: {total_imagens}")
print(f"Train: {len(imagens_train)} imagens")
print(f"Test: {len(imagens_test)} imagens")
print(f"Val: {len(imagens_val)} imagens")
