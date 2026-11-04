# Projeto de Grafos — circuito de Euler

Dante Honorato 2321406

Breno Soares 2320363

Requer Python 3 e usa apenas a biblioteca padrão.

Parâmetros do **grupo F**: `n = 10`, `p = 0,30` e `seed = 641`. Use esses mesmos valores nos dois experimentos.

Execute na pasta do projeto:

```powershell
python -X utf8 main.py 0.30 641
```

A opção `-X utf8` preserva os acentos na saída do terminal.

No macOS ou Linux, use `python3` no lugar de `python`, se necessário.

O programa gera grafos com 10 vértices até encontrar o primeiro com circuito de Euler, imprime o grafo e valida o circuito. Em seguida, reinicia o gerador com a mesma seed e avalia exatamente 1.000 grafos, exibindo a quantidade, a proporção e o tempo de geração. A classificação dos grafos ocorre depois da medição. O programa aceita `0 < p < 1`, mas os experimentos do grupo F devem usar exclusivamente `p = 0.30` e `seed = 641`.

Um grafo sem arestas tem conectividade dos vértices não isolados satisfeita por vacuidade, mas o programa não o considera solução de inspeção: não há ruas a percorrer. Vértices isolados em um grafo que tem arestas não impedem um circuito entre os demais.
