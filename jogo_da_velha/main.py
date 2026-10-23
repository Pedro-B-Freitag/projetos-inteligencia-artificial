import matplotlib.pyplot as plt
from matplotlib.widgets import Button

matriz = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

COR = (255, 255, 255)

tamanho = 3
rodadas = 0
fim_de_jogo = False
marcas = []

def montar_imagem(matriz):
    imagem = []
    for linha in matriz:
        linha_de_cores = []
        for valor in linha:
            linha_de_cores.append(COR)
        imagem.append(linha_de_cores)
    return imagem


def desenhar_marca(linha, coluna, valor):
    if valor == 1:
        marca, = ax.plot(coluna, linha, marker="x", color="blue",
                         markersize=40, markeredgewidth=5, zorder=4)
    else:
        marca, = ax.plot(coluna, linha, marker="o", color="red",
                         markersize=40, markeredgewidth=5, markerfacecolor="none", zorder=4)
    marcas.append(marca)


def verificar_vencedor():
    combinacoes = []

    for i in range(tamanho):
        combinacoes.append([matriz[i][j] for j in range(tamanho)])   # linha i
        combinacoes.append([matriz[j][i] for j in range(tamanho)])   # coluna i

    combinacoes.append([matriz[i][i] for i in range(tamanho)])
    combinacoes.append([matriz[i][tamanho - 1 - i] for i in range(tamanho)])

    for c in combinacoes:
        if c[0] != 0 and all(v == c[0] for v in c):
            return c[0]

    if rodadas == tamanho * tamanho:
        return -1

    return 0


def ao_clicar(evento):
    global rodadas, fim_de_jogo

    if fim_de_jogo or evento.inaxes != ax:
        return

    coluna = round(evento.xdata)
    linha = round(evento.ydata)

    if 0 <= linha < tamanho and 0 <= coluna < tamanho:
        if matriz[linha][coluna] > 0:
            print("Célula já marcada!")
            return

        if rodadas % 2 == 0:
            matriz[linha][coluna] = 1
        else:
            matriz[linha][coluna] = 2

        rodadas += 1
        desenhar_marca(linha, coluna, matriz[linha][coluna])

        resultado = verificar_vencedor()
        if resultado == 1:
            ax.set_title("X venceu!", fontsize=20)
            fim_de_jogo = True
        elif resultado == 2:
            ax.set_title("O venceu!", fontsize=20)
            fim_de_jogo = True
        elif resultado == -1:
            ax.set_title("Empate!", fontsize=20)
            fim_de_jogo = True

        fig.canvas.draw_idle()


def reiniciar(evento):
    global rodadas, fim_de_jogo

    for i in range(tamanho):
        for j in range(tamanho):
            matriz[i][j] = 0

    for marca in marcas:
        marca.remove()
    marcas.clear()

    rodadas = 0
    fim_de_jogo = False
    ax.set_title("")
    fig.canvas.draw_idle()


plt.ion()
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

img = ax.imshow(montar_imagem(matriz))

for i in range(tamanho + 1):
    ax.axhline(i - 0.5, color="black", linewidth=1, zorder=3)
    ax.axvline(i - 0.5, color="black", linewidth=1, zorder=3)

ax.set_xticks([])
ax.set_yticks([])

ax_botao = fig.add_axes([0.4, 0.05, 0.2, 0.075])
botao = Button(ax_botao, "Reiniciar")
botao.on_clicked(reiniciar)

fig.canvas.mpl_connect("button_press_event", ao_clicar)

while plt.fignum_exists(fig.number):
    plt.pause(0.5)