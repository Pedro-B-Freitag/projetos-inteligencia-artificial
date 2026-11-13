import os

import numpy as np
import matplotlib.pyplot as plt


script_dir = os.path.dirname(os.path.abspath(__file__))


def carregar_cidades(caminho):
    try:
        import scipy.io

        dados = scipy.io.loadmat(caminho)
        if 'x' in dados and 'y' in dados:
            x = np.asarray(dados['x'], dtype=float).ravel()
            y = np.asarray(dados['y'], dtype=float).ravel()
            return x, y
    except Exception:
        pass

    x = []
    y = []
    eixo_atual = None

    with open(caminho, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            texto = linha.strip()
            if not texto:
                continue

            if texto.startswith('# name:'):
                nome = texto.split(':', 1)[1].strip()
                if nome == 'x':
                    eixo_atual = 'x'
                elif nome == 'y':
                    eixo_atual = 'y'
                else:
                    eixo_atual = None
                continue

            if texto.startswith('#'):
                continue

            try:
                valores = np.fromstring(texto, sep=' ', dtype=float)
            except ValueError:
                continue

            if valores.size == 0:
                continue

            if eixo_atual == 'x':
                x.extend(valores.tolist())
            elif eixo_atual == 'y':
                y.extend(valores.tolist())

    if len(x) == 0 or len(y) == 0:
        raise ValueError('Arquivo de cidades inválido ou vazio')

    return np.asarray(x, dtype=float), np.asarray(y, dtype=float)


x, y = carregar_cidades(os.path.join(script_dir, 'cidades.mat'))


def cvfun(pop, x, y):
    pop = np.asarray(pop, dtype=int)
    Npop, Ncidade = pop.shape

    tour = np.hstack([pop, pop[:, [0]]])

    dcidade = np.zeros((Ncidade, Ncidade))
    for i in range(Ncidade):
        for j in range(Ncidade):
            dcidade[i, j] = np.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2)

    dist = np.zeros((Npop, 1))
    for i in range(Npop):
        for j in range(Ncidade):
            dist[i, 0] += dcidade[tour[i, j], tour[i, j + 1]]

    return dist


pesos = np.arange(10, 0, -1)
acumulado = np.cumsum(pesos)


def gerar_roleta():
    r = np.random.randint(1, acumulado[-1] + 1)
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
    return individuo


if __name__ == '__main__':
    ncidade = len(x)
    npop = 20
    iteracoes = 10000

    pop = np.array([np.random.permutation(ncidade) for _ in range(npop)])
    pop_inicial = pop.copy()

    for _ in range(iteracoes):
        distancias = cvfun(pop, x, y)
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

    print('Tamanho da População:', npop)
    print('\nPopulação Inicial:\n', pop_inicial + 1)
    print('\nPopulação Final:\n', pop + 1)
    print('\nNúmero de Cidades:', ncidade)
    print('\nMelhor Custo:', melhor_custo)
    print('\nMelhor Solução:', melhor_solucao + 1)

    caminho = np.append(melhor_solucao, melhor_solucao[0])
    plt.plot(x[caminho], y[caminho], 'b-')
    plt.plot(x, y, 'ro')
    for i in range(ncidade):
        plt.text(x[i] + 0.01, y[i] + 0.01, str(i + 1))
    plt.title(f'Melhor caminho - custo {melhor_custo:.4f}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
