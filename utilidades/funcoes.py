import pandas as pd
import requests


def ler_arquivo_investimentos():
    arquivo = pd.read_excel('utilidades/compra_cripto.xlsx')
    
    return arquivo


def nomes_moedas():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    resposta = requests.get(url)
    data = resposta.json()
    pares_brl = []
    lista_criptos = []

    #Percorre cada par de criptomoedas retornado pela API
    for symbol in data['symbols']:
        if 'BRL' in symbol['symbol']:
            pares_brl.append(symbol['symbol'])
    #remove BRL dos pares para exibir        
    for c in pares_brl:
        lista_criptos.append(c[:c.find('BRL')])
    lista_criptos.insert(0, 'Selecione a moeda')
    return lista_criptos
    

def cotar_moeda(moeda):
    if not moeda == 'Selecione a moeda':
        # Endpoint público da Binance para consultar o preço de um par de criptomoedas
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={moeda}BRL"

        response = requests.get(url)
        preco_btc = response.json()
        
        return preco_btc['price']
    else:
        preco_btc = 0

        return preco_btc


