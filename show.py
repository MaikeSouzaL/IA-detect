import cv2
import os
import uuid

# Caminho base onde os arquivos estão localizados
pasta_base = "imgBase"
pasta_saida = "output"

# Verificar se as pastas existem, caso contrário, criar
if not os.path.exists(pasta_base):
    os.makedirs(pasta_base)
    print(f"Pasta '{pasta_base}' criada. Coloque suas imagens ou vídeos nela.")

if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)
    print(f"Pasta '{pasta_saida}' criada para salvar as capturas de imagens.")

# Menu para o usuário escolher
print("Selecione uma opção:")
print("1 - Abrir uma imagem")
print("2 - Abrir um vídeo")

# Receber a entrada do usuário
opcao = input("Digite sua escolha (1 ou 2): ")

if opcao == "1":
    # Abrir uma imagem
    nome_imagem = input("Digite o nome da imagem (ex: exemplo.jpg): ")
    caminho_imagem = os.path.join(pasta_base, nome_imagem)

    # Tentar carregar a imagem
    imagem = cv2.imread(caminho_imagem)

    if imagem is None:
        print(f"Erro: Não foi possível carregar a imagem '{nome_imagem}'. Verifique se o arquivo existe na pasta '{pasta_base}'.")
    else:
        # Exibir a imagem
        cv2.imshow("Imagem", imagem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

elif opcao == "2":
    # Abrir um vídeo
    nome_video = input("Digite o nome do vídeo (ex: exemplo.mp4): ")
    caminho_video = os.path.join(pasta_base, nome_video)

    # Tentar carregar o vídeo
    video = cv2.VideoCapture(caminho_video)

    if not video.isOpened():
        print(f"Erro: Não foi possível carregar o vídeo '{nome_video}'. Verifique se o arquivo existe na pasta '{pasta_base}'.")
    else:
        # Ajustar velocidade do vídeo
        fps = int(video.get(cv2.CAP_PROP_FPS))  # Obter o FPS do vídeo
        fator_velocidade = float(input("Digite o fator de velocidade (ex: 0.5 para mais rápido, 1 para normal, 2 para mais lento): "))
        delay = max(1, int((1000 / fps) * fator_velocidade))  # Ajusta o delay para controlar a velocidade

        pausado = False
        while True:
            if not pausado:
                ret, frame = video.read()
                if not ret:
                    break

                # Exibir o frame do vídeo
                cv2.imshow("Vídeo", frame)

            # Capturar a tecla pressionada
            tecla = cv2.waitKey(1) & 0xFF

            if tecla == ord('q'):  # Parar o vídeo ao pressionar 'q'
                break
            elif tecla == ord(' '):  # Pausar/continuar ao pressionar espaço
                pausado = not pausado
            elif tecla == ord('s'):  # Capturar a imagem ao pressionar 's'
                nome_imagem = f"captura_{uuid.uuid4().hex}.jpg"
                caminho_imagem_saida = os.path.join(pasta_saida, nome_imagem)
                cv2.imwrite(caminho_imagem_saida, frame)
                print(f"Imagem capturada e salva em '{caminho_imagem_saida}'.")

            # Enquanto pausado, continuar verificando as teclas
            while pausado:
                tecla_pausa = cv2.waitKey(1) & 0xFF
                if tecla_pausa == ord(' '):  # Continuar ao pressionar espaço
                    pausado = False
                elif tecla_pausa == ord('q'):  # Parar o vídeo ao pressionar 'q'
                    pausado = False
                    break
                elif tecla_pausa == ord('s'):  # Capturar a imagem ao pressionar 's'
                    nome_imagem = f"captura_{uuid.uuid4().hex}.jpg"
                    caminho_imagem_saida = os.path.join(pasta_saida, nome_imagem)
                    cv2.imwrite(caminho_imagem_saida, frame)
                    print(f"Imagem capturada e salva em '{caminho_imagem_saida}'.")

        # Libera os recursos
        video.release()
        cv2.destroyAllWindows()

else:
    print("Opção inválida. Por favor, digite 1 para imagem ou 2 para vídeo.")
