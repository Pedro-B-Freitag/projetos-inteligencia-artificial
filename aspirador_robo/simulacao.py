from agente import executar_operacao
from quarto import Quarto
from visualizacao import mostrar_quarto

quarto = Quarto()
quarto.exibir()
mostrar_quarto(quarto)

while True:
    percepcao = quarto.percepcao()

    proximaAcao = executar_operacao(percepcao)

    if proximaAcao == "ASPIRAR":
        quarto.aspirar()
    else:
        quarto.mover(proximaAcao)

    mostrar_quarto(quarto)
