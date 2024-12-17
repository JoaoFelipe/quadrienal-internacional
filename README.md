# Análise colaborações

Esse projeto analisa colaborações de pesquisadores, buscando identificar colaboradores internacionais

## Como executar:

1- Baixe dblp.xml.gz de https://dblp.uni-trier.de/xml/ e extraia dblp.xml (preferencialmente no diretório `input`)

```
$ wget -P input https://dblp.uni-trier.de/xml/dblp.xml.gz
$ gunzip input/dblp.xml.gz
```

2. Execute `1.create_dblp_pid_map.py` para criar um mapa de todos autores que estão no DBLP em `output/dblp_map.json`

```
$ python 1.create_dblp_pid_map.py
```

3. Prepare as listas de professores de cada ano. No exemplo a seguir, estou baixando as listas de 2021 a 2024 do projeto `perfil`:

```
$ wget -P input https://github.com/gems-uff/perfil/raw/refs/heads/master/resources/affiliations/2021
$ wget -P input https://github.com/gems-uff/perfil/raw/refs/heads/master/resources/affiliations/2022
$ wget -P input https://github.com/gems-uff/perfil/raw/refs/heads/master/resources/affiliations/2023
$ wget -P input https://github.com/gems-uff/perfil/raw/refs/heads/master/resources/affiliations/2024
```

4. Execute `2.filter_current_professors.py` para filtrar o mapa do dblp e incluir apenas os professores selecionados:

```
$ python 2.filter_current_professors.py -i input/2021 input/2022 input/2023 input/2024 --read-manual-map
```

A opção `--read-manual-map` está indicando que o script deve ler automaticamente os professores não encontrados de `input/manual_map.csv`. Essa tabela pode conter mais professores do que o arquivo txt de entrada: apenas os que estiverem no txt serão selecionados.

Se ainda faltar algum professor após o filtro, o script perguntará se você deseja carregar `input/manual_map.csv` novamente. Atualize-o com os professores que faltam e confirme.

5. Execute `3.download_professor_pids.py` para baixar páginas XML de cada professor do DBLP.

```
$ python 3.download_professor_pids.py
```

(Em teoria, daria para fazer a análise diretamente pelo arquivo geral `dblp.xml`, mas processar todas as publicações de um arquivo com 4GB foi complicado - mesmo com sax - e achei mais simples obter páginas individuais)

6. Execute `4.extract_publications_and_collaborators.py` para extrair publicações e colaboradores dos professores

```
$ python 4.extract_publications_and_collaborators.py -y 2021 2022 2023 2024
```