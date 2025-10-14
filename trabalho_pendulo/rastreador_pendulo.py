import cv2
import numpy as np
import csv

caminho_video = 'pendulo.mp4'

arquivo_saida_csv = 'dados_pendulo.csv'

# HSV significa Hue (Matiz), Saturation (Saturação), Value (Valor/Brilho).

cor_inferior_hsv = np.array([25, 80, 80])
cor_superior_hsv = np.array([65, 255, 255])
# -----------------------------------------------------------------

# Tenta abrir o ficheiro de vídeo.
video = cv2.VideoCapture(caminho_video)

# Verifica se o vídeo foi aberto com sucesso.
if not video.isOpened():
    print("Erro: Não foi possível abrir o ficheiro de vídeo.")
    exit()

# Abre o ficheiro CSV em modo de escrita ('w').

with open(arquivo_saida_csv, 'w', newline='') as f:
    # Cria um objeto 'writer' para escrever no ficheiro CSV.
    writer = csv.writer(f)
    # Escreve o cabeçalho do nosso ficheiro.
    writer.writerow(['frame', 'x', 'y'])

    # Variável para contar o número do frame.
    numero_frame = 0

    print("Processando o vídeo... Pressione 'q' para sair.")

    # -------------------------------------
    while True:
        # Lê o próximo frame do vídeo. 'ok' será True se a leitura for bem-sucedida.
        ok, frame = video.read()

        # Se 'ok' for False, significa que chegámos ao fim do vídeo.
        if not ok:
            break

        # Converte o frame do espaço de cor BGR (padrão do OpenCV) para HSV.
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Cria uma 'máscara'. É uma imagem a preto e branco.
        mascara = cv2.inRange(hsv, cor_inferior_hsv, cor_superior_hsv)

        # Encontra os contornos dos objetos brancos na máscara.

        contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Verifica se algum contorno foi encontrado.
        if len(contornos) > 0:
            # Encontra o maior contorno (assumimos que é a nossa bola).
            maior_contorno = max(contornos, key=cv2.contourArea)

            # Calcula o centro do contorno usando 'momentos de imagem'.
            # Esta é uma forma matemática de obter o centro de massa de uma forma.
            M = cv2.moments(maior_contorno)
            if M["m00"] != 0:
                # Calcula a coordenada x do centro.
                centro_x = int(M["m10"] / M["m00"])
                # Calcula a coordenada y do centro.
                centro_y = int(M["m01"] / M["m00"])

                # Guarda os dados no ficheiro CSV.
                writer.writerow([numero_frame, centro_x, centro_y])

                Desenha um círculo no centro da bola e um ponto no centro.
                cv2.circle(frame, (centro_x, centro_y), 20, (0, 255, 0), 2) # Círculo verde
                cv2.circle(frame, (centro_x, centro_y), 3, (0, 0, 255), -1) # Ponto vermelho
            else:
                writer.writerow([numero_frame, '', ''])
        else:
            # Se nenhum contorno for encontrado, guarda uma linha vazia.
            writer.writerow([numero_frame, '', ''])

        # Mostra o frame com o círculo desenhado numa janela.
        cv2.imshow('Rastreamento do Pêndulo', frame)
        # Mostra a máscara numa outra janela (útil para depuração).
        cv2.imshow('Mascara de Cor', mascara)

        # Incrementa o contador de frames.
        numero_frame += 1

        # Espera por 1 milissegundo. Se a tecla 'q' for pressionada, o loop termina.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# -------------------------------------

# Liberta o ficheiro de vídeo da memória.
video.release()
# Fecha todas as janelas abertas pelo OpenCV.
cv2.destroyAllWindows()

print(f"\nProcessamento concluído! Os dados foram guardados em '{arquivo_saida_csv}'.")