# importando as bibliotecas para o projeto
import re
import pandas as pd

from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def coletar_dados(pagina):

    # Buscando todas as hospedagens da página e coletando as informações
    pagina = BeautifulSoup(pagina, "html.parser")
    for hospedagem in pagina.find_all("div", {"itemprop": "itemListElement"}):
        link = hospedagem.find("meta", {"itemprop": "url"})['content']
        nome = hospedagem.find("div", {"data-testid": "listing-card-title"}).text
        info = hospedagem.find("meta", {"itemprop": "name"})['content']
        preco = (hospedagem.find_all("span", string=re.compile(r'R\$.*'))[0].text).split("$")

        try:
            nota = (hospedagem.find_all("span", {"aria-hidden": "true"})[-1].text).split()
            if "Novo" in nota: nota = ["Sem nota", "(0)"]
        except:
            nota = ["Sem nota", "(0)"]
             

        # Dicionario com todos os dados coletados
        dados = {"Link": link, "Nome": nome, "Info": info, "Preco por noite": preco[-1], "Nota": nota[0], "N Avaliacoes": nota[-1]}

        lista_hospedagem.append(dados)

# Criando as opções de tamanho da tela
options = Options()
options.add_argument('window-size=1200,900')

# Criando o navegador, que acessa o site do airbnb
navegador = webdriver.Chrome(options=options)
navegador.get("https://www.airbnb.com.br/")
sleep(3.5)

# Clicando em aceito cookies
cookie = navegador.find_elements(By.TAG_NAME, 'button')[-1]
cookie.click()
sleep(0.5)

# Abrindo a caixa de pesquisa
btn_pesquisa = navegador.find_element(By.CSS_SELECTOR, "button > div")
btn_pesquisa.click()
sleep(1)

# Pesquisando São Paulo
input_area = navegador.find_element(By.NAME, "query")
input_area.send_keys("São Paulo")
input_area.submit()
sleep(2)

# Lista vazia para guardas as hospedagens
lista_hospedagem = []
coletar_dados(navegador.page_source)
sleep(3)

# Coletando dados das 5 primeiras páginas SE houver
for i in range(2, 6):
    proxima_pagina = navegador.find_element(By.XPATH, f'//a[text()="{i}"]')

    if proxima_pagina:
        proxima_pagina.click()
        sleep(3)
        coletar_dados(navegador.page_source)
        sleep(1.5)
    else: break



# Criando um data frame com a lista de hospedagens
df = pd.DataFrame(lista_hospedagem)

# importando para o excel
df.to_excel("hospedagens.xlsx", index=False)