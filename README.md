# Projeto de Grafos — circuito de Euler

Requer Python 3 e usa apenas a biblioteca padrão.

Execute na pasta do projeto com os valores de **p** e **seed** atribuídos ao grupo:

```powershell
python -X utf8 main.py 0.30 641
```

A opção `-X utf8` preserva os acentos na saída do terminal.

O programa gera grafos com 10 vértices até encontrar o primeiro com circuito de Euler, imprime o grafo e valida o circuito. Em seguida, reinicia o gerador com a mesma seed e avalia exatamente 1.000 grafos, exibindo a quantidade, a proporção e o tempo. Use `0 < p < 1`; com `p = 0` ou `p = 1`, não há solução para este experimento com 10 vértices.

Para executar os testes obrigatórios e adicionais:

```powershell
python -m unittest -v test_grafos
```

Um grafo sem arestas tem conectividade dos vértices não isolados satisfeita por vacuidade, mas o programa não o considera solução de inspeção: não há ruas a percorrer. Vértices isolados em um grafo que tem arestas não impedem um circuito entre os demais.

O [relatório](RELATORIO.md) contém os resultados obtidos com esses parâmetros.
