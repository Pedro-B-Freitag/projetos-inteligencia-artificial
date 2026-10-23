import matplotlib.pyplot as plt

from quarto import Quarto

CORES = {
    0: (255, 255, 255),  # limpo
    1: (74, 74, 74),     # parede
    2: (139, 94, 52),    # sujo - marrom
}

def montar_imagem(matriz):
    imagem = []
    for linha in matriz:
        linha_de_cores = []
        for valor in linha:
            linha_de_cores.append(CORES[valor])
        imagem.append(linha_de_cores)
    return imagem


def mostrar_quarto(quarto: Quarto):
    imagem = montar_imagem(quarto.matriz)

    ax = plt.gca()
    ax.imshow(imagem)

    tamanho = quarto.TAMANHO
    ax.set_xticks([x - 0.5 for x in range(tamanho + 1)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(tamanho + 1)], minor=True)
    ax.grid(which="minor", color="black", linewidth=1)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)

    ax.plot(quarto.robo_coluna, quarto.robo_linha, marker="o", color="red", markersize=30)

    plt.pause(0.5)
    plt.clf()