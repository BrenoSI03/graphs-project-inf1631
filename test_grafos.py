import random
import unittest

from main import circuito_euler, conexo, euleriano, gerar_grafo, graus, valida_circuito


class TestesGrafos(unittest.TestCase):
    def test_ciclo_c4(self):
        grafo = {1: {2, 4}, 2: {1, 3}, 3: {2, 4}, 4: {1, 3}}
        original = {vertice: vizinhos.copy() for vertice, vizinhos in grafo.items()}
        circuito = circuito_euler(grafo)
        self.assertEqual(graus(grafo), {1: 2, 2: 2, 3: 2, 4: 2})
        self.assertTrue(conexo(grafo))
        self.assertTrue(euleriano(grafo))
        self.assertTrue(valida_circuito(grafo, circuito))
        self.assertEqual(grafo, original)

    def test_caminho_p4(self):
        grafo = {1: {2}, 2: {1, 3}, 3: {2, 4}, 4: {3}}
        self.assertTrue(conexo(grafo))
        self.assertFalse(euleriano(grafo))
        self.assertIsNone(circuito_euler(grafo))

    def test_duas_componentes_ciclicas(self):
        grafo = {
            1: {2, 3}, 2: {1, 3}, 3: {1, 2},
            4: {5, 6}, 5: {4, 6}, 6: {4, 5},
        }
        self.assertFalse(conexo(grafo))
        self.assertFalse(euleriano(grafo))

    def test_grafo_sem_arestas(self):
        grafo = {1: set(), 2: set()}
        self.assertTrue(conexo(grafo))
        self.assertFalse(euleriano(grafo))
        self.assertIsNone(circuito_euler(grafo))
        self.assertFalse(valida_circuito(grafo, []))

    def test_isolado_nao_impede_circuito(self):
        grafo = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}, 4: set()}
        self.assertTrue(conexo(grafo))
        self.assertTrue(valida_circuito(grafo, circuito_euler(grafo)))

    def test_validacao_rejeita_arestas_ausentes_e_repetidas(self):
        grafo = {1: {2, 3}, 2: {1, 3}, 3: {1, 2}}
        self.assertFalse(valida_circuito(grafo, [1, 2, 1, 3]))
        self.assertFalse(valida_circuito(grafo, [1, 2, 4, 1]))
        self.assertFalse(valida_circuito(grafo, [1, 2, 3]))

    def test_geracao_reprodutivel_e_extremos(self):
        self.assertEqual(gerar_grafo(10, 0.3, random.Random(137)),
                         gerar_grafo(10, 0.3, random.Random(137)))
        self.assertEqual(sum(graus(gerar_grafo(4, 0)).values()), 0)
        self.assertEqual(sum(graus(gerar_grafo(4, 1)).values()), 12)
        with self.assertRaises(ValueError):
            gerar_grafo(4, -0.1)


if __name__ == "__main__":
    unittest.main()
