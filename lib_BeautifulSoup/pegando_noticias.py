import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fazendo um get da página inicial do g1
url = requests.get("https://g1.globo.com/")

# Criando um objeto BeautifulSoup, usando o conteudo do site
site = BeautifulSoup(url.content, "html.parser")

# Lista vazia, para armazenar as noticias
lista_noticias = []

# Percorrendo todas as noticias da página inicial
for noticia in site.find_all("div", attrs={"class": "feed-post-body"}):

    # Pegando o titulo, subtitulo e header
    titulo = noticia.find("a", attrs={"class": "feed-post-link"})
    subtitulo = noticia.find("div", attrs={"class": "feed-post-body-resumo"})

    dicionario = {"titulo": titulo.text, "link": titulo['href']}

    # Algumas vezes a noticia não possuo subtitulo
    if subtitulo:
        dicionario["subtitulo"] = subtitulo.text

    # Salvando um dicionario com as informações na lista
    lista_noticias.append(dicionario)

tabela = pd.DataFrame(lista_noticias)
tabela.to_csv("noticias.csv", sep=';', index=False)