# Algoritmo_recomendacao
Desenvolvi um algoritmo de recomendação de projetos em python, em sincronia com o firebase.
O algoritmo tem como base o tempo de acesso de um usuario a determinado projeto, de forma que o algoritmo consome tempo de entrada e tempo de saida do usuario a cada projeto especifico, com isso os dados desse projeto acessado sao analisados por uma NLP(Natural Language Processing) para contar quantas palavras tem, desta forma se obtem o tempo de medio de leitura dentro da pagina do projeto e efetua a comparacao com o tempo de permanencia do usuario.

Inicialmente desenvolvi em duas partes:
1 - Consumindo e dando update no BD
2 - Consumindo e dando update no BD

Por fim, decidi unir ambos os algoritmos, tornando-os um so, para executar somente uma vez.
