import requests
import pandas as pd
from bs4 import BeautifulSoup

# Url base do mercado livre
base = "https://lista.mercadolivre.com.br/"

# Produto a ser procurado
produto = input("Digite o nome do produto: ").strip().lower()

# Response da busca do produto
response = requests.get(base + produto)

# Criando o objeti BeautifulSoup
site = BeautifulSoup(response.text, "html.parser")

# Lista vazia que vai armazenar os produtos
lista_produtos = []

# Procurando a página dos produtos
for produto in site.find_all("div", attrs={"class": "ui-search-result__content-wrapper shops__result-content-wrapper"}):

    # Filtrando produto
    nome = produto.find("h2", attrs={"class": "ui-search-item__title"})
    link = produto.find("a", attrs={"class": "ui-search-link"})
    preco = produto.find("span", attrs={"class": "andes-money-amount__fraction"})
    frete = produto.find("div", attrs={"class": "ui-pb-container"})

    # Criando um dicionario com as infos de cada produto
    dicionario = {"Link": link['href'], "Nome": nome.text, "Preco": preco.text}

    # Se a informação do frete for Vazia OU diferente de 'Frete grátis' recebe 'Não', caso seja 'Frete Grátis' recebe 'Sim
    if frete is None or frete.text != "Frete grátis":
        dicionario['Frete Grátis'] = "Não"
    else:
        dicionario['Frete Grátis'] = "Sim"

    lista_produtos.append(dicionario)


tabela = pd.DataFrame(lista_produtos)
tabela.to_csv("produtos.csv", sep=';', index=False)
tabela.to_excel("produtos.xlsx", index=False)

