from quarto import Quarto as quarto

TAMANHO_SALA = quarto.TAMANHO - 2

def mapear_percepcao(percepcao):
    linha = percepcao[0]
    coluna = percepcao[1]
    sujo = percepcao[2]
    return linha, coluna, sujo


def executar_operacao(percepcao):
    linha, coluna, sujo = mapear_percepcao(percepcao)

    if sujo:
        return "ASPIRAR"

    if coluna == 1:
        if linha > 1:
            return "ACIMA"
        else:
            return "DIREITA"

    linha_par = linha % 2 == 0

    if linha_par:
        if coluna > 2:
            return "ESQUERDA"
        elif linha < TAMANHO_SALA:
            return "ABAIXO"
        else:
            return "ESQUERDA"

    if coluna < TAMANHO_SALA:
        return "DIREITA"
    else:
        return "ABAIXO"

def checar_quarto(sala):
    for linha in sala:
        for valor in linha:
            if valor == quarto.SUJO:
                return 1
    return 0

sala_conhecida = None
plano_de_acoes = []

def definir_sala(matriz):
    global sala_conhecida
    sala_conhecida = matriz

def encontrar_sujeiras(sala):
    posicoes = []
    for indice_linha in range(len(sala)):
        for indice_coluna in range(len(sala[indice_linha])):
            if sala[indice_linha][indice_coluna] == quarto.SUJO:
                posicoes.append((indice_linha, indice_coluna))
    return posicoes


def distancia(ponto_a, ponto_b):
    linha_a, coluna_a = ponto_a
    linha_b, coluna_b = ponto_b
    return abs(linha_a - linha_b) + abs(coluna_a - coluna_b)


def calcular_melhor_ordem(inicio, sujeiras):
    restantes = list(sujeiras)
    ordem_pontos = []
    posicao_atual = inicio

    while len(restantes) > 0:
        mais_perto = restantes[0]
        menor_distancia = distancia(posicao_atual, mais_perto)

        for ponto in restantes:
            distancia_ate_ponto = distancia(posicao_atual, ponto)
            if distancia_ate_ponto < menor_distancia:
                mais_perto = ponto
                menor_distancia = distancia_ate_ponto

        ordem_pontos.append(mais_perto)
        restantes.remove(mais_perto)
        posicao_atual = mais_perto

    return ordem_pontos


def construir_plano_de_acoes(inicio, ordem_de_pontos):
    acoes = []
    linha_atual, coluna_atual = inicio

    for ponto in ordem_de_pontos:
        linha_alvo, coluna_alvo = ponto

        while linha_atual != linha_alvo:
            if linha_atual < linha_alvo:
                acoes.append("ABAIXO")
                linha_atual = linha_atual + 1
            else:
                acoes.append("ACIMA")
                linha_atual = linha_atual - 1

        while coluna_atual != coluna_alvo:
            if coluna_atual < coluna_alvo:
                acoes.append("DIREITA")
                coluna_atual = coluna_atual + 1
            else:
                acoes.append("ESQUERDA")
                coluna_atual = coluna_atual - 1

        acoes.append("ASPIRAR")

    return acoes


def agenteObjetivo(percepcao, objObtido):
    global plano_de_acoes

    if objObtido == 0:
        plano_de_acoes = []
        return "NoOp"

    if len(plano_de_acoes) == 0:
        linha, coluna, sujo = mapear_percepcao(percepcao)
        sujeiras = encontrar_sujeiras(sala_conhecida)
        ordem_de_pontos = calcular_melhor_ordem((linha, coluna), sujeiras)
        plano_de_acoes = construir_plano_de_acoes((linha, coluna), ordem_de_pontos)

    proxima_acao = plano_de_acoes[0]
    plano_de_acoes = plano_de_acoes[1:]

    return proxima_acao

