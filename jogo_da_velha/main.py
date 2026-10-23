"""
Jogo escolhido: Jogo da Velha. Regra: vence quem alinhar 3 símbolos iguais.

Estado inicial: matriz 3x3 vazia.

Jogadores: 2 jogadores, MAX (agente, O) e MIN (humano, X).

Ações possíveis: posicionar o seu símbolo em uma posição não ocupada da matriz.

Função de transição: estado atual + ação = matriz atualizada com o novo símbolo
na posição escolhida.

Estado terminal: quando há 3 símbolos iguais alinhados (na horizontal, vertical
ou diagonal), o que é vitória, ou quando a matriz está cheia sem alinhamento,
o que é empate.

Função de utilidade (do ponto de vista de MAX): vitória = +1, empate = 0,
derrota = -1.

Tipo de jogo: determinístico (não há sorte), de soma zero, com informação
perfeita e jogadas alternadas.

Algoritmo de busca competitiva: Minimax.

Representação em Python: uma matriz 3x3 (lista de listas), onde 0 é uma casa
vazia, 1 é o X (humano) e 2 é o O (agente).

Ações válidas e término: as ações válidas são as casas com valor 0. A função
verificar_vencedor() olha todas as linhas, colunas e diagonais e também se a
matriz está cheia.

Escolha da jogada: o agente testa cada casa vazia e simula o resto do jogo com
o Minimax, supondo que o humano sempre faz a melhor jogada para ele. No fim,
escolhe a casa com a maior pontuação.

Reflexão do grupo: o Minimax foi adequado porque o jogo é pequeno (no máximo 9! jogadas
possíveis), então dá para explorar a árvore inteira e o agente nunca perde.
A limitação é que ele visita estados repetidos e ramos desnecessários. A poda
Alfa-Beta daria o mesmo resultado olhando bem menos estados, e em jogos maiores
(damas, xadrez) seria preciso ainda limitar a profundidade e usar uma função de
avaliação heurística.
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Valores que cada casa da matriz pode ter
VAZIO = 0
HUMANO = 1   # X, jogador MIN
AGENTE = 2   # O, jogador MAX
EMPATE = -1  # usado só como resultado de verificar_vencedor()

tamanho = 3

# Estado inicial: matriz 3x3 vazia
matriz = [[VAZIO] * tamanho for _ in range(tamanho)]

fim_de_jogo = False
marcas = []  # desenhos de X e O na tela, guardados para poder apagar


def desenhar_marca(linha, coluna, jogador):
    # Desenha um X azul para o humano ou um O vermelho para o agente
    if jogador == HUMANO:
        marca, = ax.plot(coluna, linha, marker="x", color="blue",
                         markersize=40, markeredgewidth=5, zorder=4)
    else:
        marca, = ax.plot(coluna, linha, marker="o", color="red",
                         markersize=40, markeredgewidth=5, markerfacecolor="none", zorder=4)
    marcas.append(marca)


def verificar_vencedor(tabuleiro):
    # Retorna HUMANO ou AGENTE se alguém venceu, EMPATE se a matriz está cheia,
    # ou VAZIO se o jogo ainda não acabou
    combinacoes = []

    for i in range(tamanho):
        combinacoes.append([tabuleiro[i][j] for j in range(tamanho)])   # linha i
        combinacoes.append([tabuleiro[j][i] for j in range(tamanho)])   # coluna i

    combinacoes.append([tabuleiro[i][i] for i in range(tamanho)])                # diagonal principal
    combinacoes.append([tabuleiro[i][tamanho - 1 - i] for i in range(tamanho)])  # diagonal secundária

    # Alguém venceu se as 3 casas de uma combinação têm o mesmo símbolo
    for c in combinacoes:
        if c[0] != VAZIO and all(v == c[0] for v in c):
            return c[0]

    # Sem vencedor e sem casas vazias: empate
    if all(v != VAZIO for linha in tabuleiro for v in linha):
        return EMPATE

    return VAZIO


def casas_vazias(tabuleiro):
    # Ações possíveis: todas as posições ainda não ocupadas
    return [(i, j) for i in range(tamanho) for j in range(tamanho) if tabuleiro[i][j] == VAZIO]


def minimax(tabuleiro, vez_do_agente):
    # Função de utilidade: +1 se o agente vence, -1 se o humano vence, 0 se empata
    resultado = verificar_vencedor(tabuleiro)
    if resultado == AGENTE:
        return 1
    if resultado == HUMANO:
        return -1
    if resultado == EMPATE:
        return 0

    # Jogo não acabou: testa cada jogada possível e calcula seu valor
    valores = []
    for i, j in casas_vazias(tabuleiro):
        tabuleiro[i][j] = AGENTE if vez_do_agente else HUMANO  # faz a jogada
        valores.append(minimax(tabuleiro, not vez_do_agente))   # passa a vez
        tabuleiro[i][j] = VAZIO                                 # desfaz a jogada

    # MAX (agente) escolhe o maior valor, MIN (humano) escolhe o menor
    return max(valores) if vez_do_agente else min(valores)


def melhor_jogada():
    # Testa cada casa vazia e fica com a que dá o maior valor para o agente
    melhor_valor = -2  # menor que qualquer utilidade possível
    melhor = None
    for i, j in casas_vazias(matriz):
        matriz[i][j] = AGENTE
        valor = minimax(matriz, vez_do_agente=False)  # depois do agente, é a vez do humano
        matriz[i][j] = VAZIO
        if valor > melhor_valor:
            melhor_valor = valor
            melhor = (i, j)
    return melhor


def jogar(linha, coluna, jogador):
    # Função de transição: coloca o símbolo na matriz e verifica se o jogo acabou
    global fim_de_jogo

    matriz[linha][coluna] = jogador
    desenhar_marca(linha, coluna, jogador)

    resultado = verificar_vencedor(matriz)
    if resultado == HUMANO:
        ax.set_title("X venceu!", fontsize=20)
        fim_de_jogo = True
    elif resultado == AGENTE:
        ax.set_title("O venceu!", fontsize=20)
        fim_de_jogo = True
    elif resultado == EMPATE:
        ax.set_title("Empate!", fontsize=20)
        fim_de_jogo = True


def ao_clicar(evento):
    # Chamada quando o humano clica no tabuleiro
    if fim_de_jogo or evento.inaxes != ax:
        return

    # Converte a posição do clique para linha e coluna da matriz
    coluna = round(evento.xdata)
    linha = round(evento.ydata)

    if 0 <= linha < tamanho and 0 <= coluna < tamanho:
        if matriz[linha][coluna] != VAZIO:
            print("Célula já marcada!")
            return

        jogar(linha, coluna, HUMANO)

        # Se o jogo não acabou, o agente responde com a melhor jogada
        if not fim_de_jogo:
            jogar(*melhor_jogada(), AGENTE)

        fig.canvas.draw_idle()


def reiniciar(evento):
    # Volta ao estado inicial: matriz vazia e tela limpa
    global fim_de_jogo

    for i in range(tamanho):
        for j in range(tamanho):
            matriz[i][j] = VAZIO

    for marca in marcas:
        marca.remove()
    marcas.clear()

    fim_de_jogo = False
    ax.set_title("")
    fig.canvas.draw_idle()


# Monta a janela com o tabuleiro em branco
plt.ion()
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

ax.imshow([[(255, 255, 255)] * tamanho for _ in range(tamanho)])

# Desenha as linhas da grade
for i in range(tamanho + 1):
    ax.axhline(i - 0.5, color="black", linewidth=1, zorder=3)
    ax.axvline(i - 0.5, color="black", linewidth=1, zorder=3)

ax.set_xticks([])
ax.set_yticks([])

# Botão para começar uma nova partida
ax_botao = fig.add_axes([0.4, 0.05, 0.2, 0.075])
botao = Button(ax_botao, "Reiniciar")
botao.on_clicked(reiniciar)

fig.canvas.mpl_connect("button_press_event", ao_clicar)

# Mantém a janela aberta até o usuário fechar
while plt.fignum_exists(fig.number):
    plt.pause(0.5)
