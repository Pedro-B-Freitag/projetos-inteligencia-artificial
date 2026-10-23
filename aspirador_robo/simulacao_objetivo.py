from agente import agenteObjetivo, checar_quarto, definir_sala
from quarto import Quarto
from visualizacao import mostrar_quarto

quarto = Quarto(robo_linha=1, robo_coluna=1)
pontos = 0

definir_sala(quarto.matriz)

quarto.exibir()
mostrar_quarto(quarto)

while True:
    objObtido = checar_quarto(quarto.matriz)
    percepcao = quarto.percepcao()

    proximaAcao = agenteObjetivo(percepcao, objObtido)

    if proximaAcao == "NoOp":
        break

    if proximaAcao == "ASPIRAR":
        quarto.aspirar()
    else:
        quarto.mover(proximaAcao)

    pontos = pontos + 1
    mostrar_quarto(quarto)

print("Sala limpa em", pontos, "passos")
