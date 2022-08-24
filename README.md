# Videomatik Challenge - TDC Business 2022

Desafio proposto pela Videomatik durante o The Developer's Conference - Business 2022. 
[Link](https://videomatik.com.br/desafio)

## Ambiente:

### Requisitos:
- Python 3.7+

### Instalação:

Dentro da pasta raiz do projeto execute:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Execução

Para rodar cada um dos níveis, basta executar cada um dos seguintes comandos na pasta raiz do projeto:

- Nível **Easy**

```
python3 challenges/easy.py
```

Esse código gera uma exportação dos dados de cada renderização, incluindo o link para download, em `exports/easy.json`

- Nível **Medium** (Não implementado ainda)

```
python3 challenges/medium.py
```

Em ambos os casos, é necessário adicionar os dados de chave de API e demais informações necessárias no final de cada um dos scripts, no local indicado.


**OBS:** Para executar cada um dos níveis, é necessário estar com o ambiente virtual habilitado. Para isso, basta usar o seguinte comando n pasta raiz do projeto:

```
source venv/bin/activate
```

Para desativar o ambientevirtual, basta executar:

```
deactivate
```