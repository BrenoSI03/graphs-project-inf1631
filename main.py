"""Experimentos com circuitos de Euler em grafos aleatórios simples."""

import argparse
import random
import time


def gerar_grafo(n, p, gerador=None):
    """Decide independentemente a presença de cada aresta possível."""
    if n < 1 or not 0 <= p <= 1:
        raise ValueError("n deve ser positivo e p deve estar entre 0 e 1")
    if gerador is None:
        gerador = random

    grafo = {vertice: set() for vertice in range(1, n + 1)}
    for origem in range(1, n + 1):
        for destino in range(origem + 1, n + 1):
            if gerador.random() < p:
                grafo[origem].add(destino)
                grafo[destino].add(origem)
    return grafo


def graus(grafo):
    return {vertice: len(vizinhos) for vertice, vizinhos in grafo.items()}


def conexo(grafo):
    """Verifica a conectividade somente dos vértices com arestas."""
    ativos = {vertice for vertice, vizinhos in grafo.items() if vizinhos}
    if not ativos:
        return True

    inicio = next(iter(ativos))
    visitados = {inicio}
    pilha = [inicio]
    while pilha:
        vertice = pilha.pop()
        for vizinho in grafo[vertice]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                pilha.append(vizinho)
    return ativos == visitados


def euleriano(grafo):
    """Exige ruas, conectividade dos vértices ativos e graus pares."""
    graus_grafo = graus(grafo)
    ha_arestas = any(graus_grafo.values())
    return ha_arestas and conexo(grafo) and all(
        grau % 2 == 0 for grau in graus_grafo.values()
    )


def circuito_euler(grafo):
    """Constrói o circuito por Hierholzer, preservando o grafo recebido."""
    if not euleriano(grafo):
        return None

    restantes = {vertice: vizinhos.copy() for vertice, vizinhos in grafo.items()}
    inicio = next(vertice for vertice in sorted(grafo) if grafo[vertice])
    pilha = [inicio]
    circuito = []
    while pilha:
        vertice = pilha[-1]
        if restantes[vertice]:
            vizinho = min(restantes[vertice])
            restantes[vertice].remove(vizinho)
            restantes[vizinho].remove(vertice)
            pilha.append(vizinho)
        else:
            circuito.append(pilha.pop())
    circuito.reverse()
    return circuito


def valida_circuito(grafo, circuito):
    """Confere cada aresta não direcionada uma única vez."""
    if not circuito or len(circuito) < 2 or circuito[0] != circuito[-1]:
        return False

    arestas = {
        (min(origem, destino), max(origem, destino))
        for origem, vizinhos in grafo.items()
        for destino in vizinhos
    }
    if len(circuito) != len(arestas) + 1:
        return False

    percorridas = set()
    for origem, destino in zip(circuito, circuito[1:]):
        aresta = (min(origem, destino), max(origem, destino))
        if aresta not in arestas or aresta in percorridas:
            return False
        percorridas.add(aresta)
    return percorridas == arestas


def executar(p, seed):
    if not 0 < p < 1:
        raise ValueError("p deve ser maior que 0 e menor que 1 para a busca terminar")

    n = 10
    gerador = random.Random(seed)
    tentativas = 0
    while True:
        tentativas += 1
        grafo = gerar_grafo(n, p, gerador)
        if euleriano(grafo):
            break

    circuito = circuito_euler(grafo)
    arestas = sorted(
        (origem, destino)
        for origem, vizinhos in grafo.items()
        for destino in vizinhos
        if origem < destino
    )
    graus_grafo = graus(grafo)
    print("\n=== Parâmetros ===")
    print(f"Número de vértices: {n}")
    print(f"Probabilidade p: {p}")
    print(f"Seed: {seed}")

    print("\n=== Primeiro grafo Euleriano ===")
    print(f"Número de grafos gerados: {tentativas}")
    print("Adjacências:")
    for vertice in grafo:
        vizinhos = ", ".join(map(str, sorted(grafo[vertice]))) or "isolado"
        print(f"  {vertice:>2}: {vizinhos}")
    print(f"Arestas ({len(arestas)}):")
    for posicao in range(0, len(arestas), 5):
        print("  " + "  ".join(f"({u}, {v})" for u, v in arestas[posicao:posicao + 5]))
    print("Graus:")
    for vertice, grau in graus_grafo.items():
        print(f"  v{vertice}: {grau}")
    print(f"Conexo (vértices não isolados): {'sim' if conexo(grafo) else 'não'}")
    print(f"Todos os graus são pares: {'sim' if all(g % 2 == 0 for g in graus_grafo.values()) else 'não'}")
    print(f"Euleriano: {'sim' if euleriano(grafo) else 'não'}")
    print("Circuito de Euler:")
    print("  " + " -> ".join(map(str, circuito)))
    print(f"Validação do circuito: {'OK' if valida_circuito(grafo, circuito) else 'FALHOU'}")

    gerador = random.Random(seed)
    inicio = time.perf_counter()
    quantidade = 0
    for _ in range(1000):
        if euleriano(gerar_grafo(n, p, gerador)):
            quantidade += 1
    tempo = time.perf_counter() - inicio
    print("\n=== Experimento com 1000 grafos ===")
    print(f"Tempo total: {tempo:.6f} s")
    print(f"Grafos Eulerianos: {quantidade}")
    print(f"Proporção: {quantidade / 1000:.3f}")


if __name__ == "__main__":
    analisador = argparse.ArgumentParser(description="Experimentos com circuitos de Euler")
    analisador.add_argument("p", type=float, help="probabilidade de cada aresta (0 < p < 1)")
    analisador.add_argument("seed", type=int, help="semente do gerador aleatório")
    argumentos = analisador.parse_args()
    try:
        executar(argumentos.p, argumentos.seed)
    except ValueError as erro:
        analisador.error(str(erro))
