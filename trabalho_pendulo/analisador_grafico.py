# -*- coding: utf-8 -*-

# -------------------------------------
# Passo 1: Importar as bibliotecas
# -------------------------------------
# pandas: Para ler e manipular os nossos dados do ficheiro CSV de forma fácil.
# matplotlib.pyplot: Para criar e mostrar o gráfico.
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------
# Passo 2: Configurações
# -------------------------------------
# Nome do ficheiro CSV que foi gerado pelo rastreador.
arquivo_dados = 'dados_pendulo.csv'

# --- ATENÇÃO: COLOQUE AQUI O VALOR DE FPS QUE VOCÊ DESCOBRIU! ---
# Use o valor exato que o script 'descobrir_fps.py' lhe deu.
# Exemplo para um vídeo de 30 FPS.
FPS_DO_VIDEO = 30.0
# ----------------------------------------------------------------

# -------------------------------------
# Passo 3: Ler e Preparar os Dados com Pandas
# -------------------------------------
try:
    # Lê o ficheiro CSV para um 'DataFrame' do pandas.
    # Um DataFrame é como uma tabela ou folha de cálculo inteligente.
    dados = pd.read_csv(arquivo_dados)
    
    # Limpeza de dados: remove linhas onde a deteção possa ter falhado
    # (ou seja, onde 'x' ou 'y' possam estar vazios).
    dados.dropna(inplace=True)
    
    # Converte as colunas para o tipo numérico, caso não estejam.
    dados['x'] = pd.to_numeric(dados['x'])
    dados['frame'] = pd.to_numeric(dados['frame'])

    # É aqui que a mágica acontece: criar a coluna 'tempo'.
    # A operação é aplicada a todos os valores da coluna 'frame' de uma só vez.
    dados['tempo'] = dados['frame'] / FPS_DO_VIDEO

    print("Dados carregados com sucesso! A gerar o gráfico...")
    print(dados.head()) # Mostra as primeiras 5 linhas dos dados já com o tempo

    # -------------------------------------
    # Passo 4: Criar o Gráfico com Matplotlib
    # -------------------------------------
    # Cria uma figura e um eixo para o nosso gráfico.
    plt.figure(figsize=(12, 6)) # Define o tamanho do gráfico (largura, altura)

    # Plota os dados: eixo X será o nosso 'tempo', eixo Y será a posição 'x'.
    # 'o-' significa que queremos desenhar pequenos círculos ('o') em cada ponto
    # de dados e ligá-los com uma linha ('-').
    plt.plot(dados['tempo'], dados['x'], 'o-', markersize=3, label='Posição da bola')

    # Adiciona títulos e etiquetas para deixar o gráfico profissional.
    plt.title('Posição Horizontal (x) do Pêndulo em Função do Tempo')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição Horizontal (pixels)')
    plt.grid(True) # Adiciona uma grelha para facilitar a leitura.
    plt.legend() # Mostra a legenda que definimos no 'label'.

    # Mostra o gráfico numa janela.
    plt.show()

except FileNotFoundError:
    print(f"Erro: O ficheiro '{arquivo_dados}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")