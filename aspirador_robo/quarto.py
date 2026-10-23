import random

class Quarto:
    TAMANHO = 6
    PAREDE = 1
    LIMPO = 0
    SUJO = 2

    def __init__(self, robo_linha=None, robo_coluna=None):
        self.matriz = self._gerar_quarto()

        if robo_linha is None:
            robo_linha = random.randint(1, self.TAMANHO - 2)
        if robo_coluna is None:
            robo_coluna = random.randint(1, self.TAMANHO - 2)

        self.robo_linha = robo_linha
        self.robo_coluna = robo_coluna

    def _gerar_quarto(self):
        matriz = [[self.PAREDE] * self.TAMANHO for _ in range(self.TAMANHO)]

        posicoes_internas = []
        for linha in range(1, self.TAMANHO - 1):
            for coluna in range(1, self.TAMANHO - 1):
                posicoes_internas.append((linha, coluna))

        for linha, coluna in posicoes_internas:
            matriz[linha][coluna] = self.LIMPO

        qtd_sujeiras = random.randint(1, len(posicoes_internas) - 1)
        posicoes_sujas = random.sample(posicoes_internas, qtd_sujeiras)

        for linha, coluna in posicoes_sujas:
            matriz[linha][coluna] = self.SUJO

        return matriz

    def exibir(self):
        for linha in self.matriz:
            print(" ".join(str(valor) for valor in linha))

    def percepcao(self):
        sujo = self.matriz[self.robo_linha][self.robo_coluna] == self.SUJO
        return (self.robo_linha, self.robo_coluna, sujo)

    def aspirar(self):
        self.matriz[self.robo_linha][self.robo_coluna] = self.LIMPO

    def mover(self, direcao):
        nova_linha = self.robo_linha
        nova_coluna = self.robo_coluna

        if direcao == "ACIMA":
            nova_linha = nova_linha - 1
        elif direcao == "ABAIXO":
            nova_linha = nova_linha + 1
        elif direcao == "ESQUERDA":
            nova_coluna = nova_coluna - 1
        elif direcao == "DIREITA":
            nova_coluna = nova_coluna + 1

        if self.matriz[nova_linha][nova_coluna] != self.PAREDE:
            self.robo_linha = nova_linha
            self.robo_coluna = nova_coluna
