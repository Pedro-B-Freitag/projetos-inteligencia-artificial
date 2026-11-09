import numpy as np
import matplotlib.pyplot as plt

x, y = np.loadtxt('cidades.mat')

def cvfun(pop, x, y):

    pop = np.asarray(pop, dtype=int)
    Npop, Ncidade = pop.shape

    tour = np.hstack([pop, pop[:, [0]]])

    dcidade = np.zeros((Ncidade, Ncidade))
    for i in range(Ncidade):
        for j in range(Ncidade):
            dcidade[i, j] = np.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)

    dist = np.zeros((Npop, 1))
    for i in range(Npop):
        for j in range(Ncidade):
            dist[i, 0] += dcidade[tour[i, j], tour[i, j + 1]]

    return dist

pesos = np.arange(10, 0, -1)
acumulado = np.cumsum(pesos)

def gerar_roleta():
    r = np.random.randint(1,56)
    return np.searchsorted(acumulado, r)


def cruzamento_cycle(pai, mae, pos=None):
    filho1 = pai.copy()
    filho2 = mae.copy()

    if pos is None:
        pos = np.random.randint(len(pai))

    while True:
        filho1[pos], filho2[pos] = filho2[pos], filho1[pos]

        duplicado = np.where(filho1 == filho1[pos])[0]
        duplicado = duplicado[duplicado != pos]

        if len(duplicado) == 0:
            break

        pos = duplicado[0]

    return filho1, filho2


def mutacao(individuo):
    i, j = np.random.choice(len(individuo), 2, replace=False)
    individuo[i], individuo[j] = individuo[j], individuo[i]


if __name__ == "__main__":
    ncidade = len(x)
    npop = 20
    iteracoes = 10000

    pop = np.array([np.random.permutation(ncidade) for _ in range(npop)])
    pop_inicial = pop.copy()  # guarda a população inicial para mostrar no final

    for _ in range(iteracoes):
        distancias = cvfun(pop, x, y)

        # ordena do melhor (menor distância) para o pior e mantém a metade
        indices = np.argsort(distancias.flatten())
        indices = indices[:-10]
        sobreviventes = pop[indices]

        casais = []
        for _ in range(5):
            pai = sobreviventes[gerar_roleta()]
            mae = sobreviventes[gerar_roleta()]
            casais.append((pai, mae))

        filhos = []
        for pai, mae in casais:
            filho1, filho2 = cruzamento_cycle(pai, mae)
            filhos.extend([filho1, filho2])

        pop = np.vstack([sobreviventes, filhos])

        for individuo in pop[1:]:
            mutacao(individuo)

    distancias = cvfun(pop, x, y).flatten()
    ordem = np.argsort(distancias)
    pop = pop[ordem]
    melhor_custo = distancias[ordem[0]]
    melhor_solucao = pop[0]

    print("Tamanho da População:", npop)
    print("\nPopulação Inicial:\n", pop_inicial + 1)
    print("\nPopulação Final:\n", pop + 1)
    print("\nNúmero de Cidades:", ncidade)
    print("\nMelhor Custo:", melhor_custo)
    print("\nMelhor Solução:", melhor_solucao + 1)

    caminho = np.append(melhor_solucao, melhor_solucao[0])
    plt.plot(x[caminho], y[caminho], 'b-')
    plt.plot(x, y, 'ro')
    for i in range(ncidade):
        plt.text(x[i] + 0.01, y[i] + 0.01, str(i + 1))
    plt.title(f"Melhor caminho - custo {melhor_custo:.4f}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
