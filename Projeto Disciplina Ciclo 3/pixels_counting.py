from PIL import Image
import numpy as np

def processar_imagem(caminho_imagem, tamanho_pixel_metros):
    # Abrir a imagem e convertê-la para um array NumPy
    imagem = Image.open(caminho_imagem)
    imagem_array = np.array(imagem)

    # Cálculo de contagem total de pixels
    total_pixels = imagem_array.size

    # Contagem de pixels para cada classe
    pixels_sem_dados = np.sum(imagem_array == 0)
    pixels_soja = np.sum(imagem_array == 39)
    pixels_pastagem = np.sum(imagem_array == 15)

    # Remover pixels sem dados para obter o total válido
    total_valido = total_pixels - pixels_sem_dados

    # Conversão para hectares (1 hectare = 10.000 m²)
    area_soja_ha = (pixels_soja * tamanho_pixel_metros**2) / 10000
    area_pastagem_ha = (pixels_pastagem * tamanho_pixel_metros**2) / 10000

    # Resultados
    resultados = {
        "Total de pixels": total_pixels,
        "Pixels sem dados (0)": pixels_sem_dados,
        "Pixels soja (39)": pixels_soja,
        "Pixels pastagem (15)": pixels_pastagem,
        "Total válido de pixels": total_valido,
        "Área de plantio de soja (ha)": area_soja_ha,
        "Área de pastagem (ha)": area_pastagem_ha,
    }

    return resultados

# Caminho da imagem de satélite
caminho_imagem = "brasil.png" 

# Tamanho do pixel em metros (exemplo: 30x30 metros)
tamanho_pixel_metros = 30

# Chamar a função e exibir os resultados
try:
    resultados = processar_imagem(caminho_imagem, tamanho_pixel_metros)
    for chave, valor in resultados.items():
        print(f"{chave}: {valor}")
except FileNotFoundError:
    print("Erro: Imagem não encontrada. Verifique o caminho do arquivo.")
