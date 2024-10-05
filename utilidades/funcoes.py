import pandas as pd
import requests
import os


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
        preco = response.json()
        
        return preco['price']
    else:
        preco = 0

        return preco


def ler_arquivo_investimentos():
    caminho_arquivo = 'utilidades/compra_cripto.xlsx'
    
    if not os.path.exists(caminho_arquivo):
        df_padrao = pd.DataFrame({
            'moeda': [],
            'transacao': [],
            'data_transacao': [],
            'cotacao_na_data': [],
            'valor_comprado': [],
            'total_comprado': []
        })
        
        df_padrao.to_excel(caminho_arquivo, index=False)
        print(f'Arquivo \"{caminho_arquivo}\" criado com colunas padrão.')
    
    arquivo = pd.read_excel(caminho_arquivo)
    arquivo['data_transacao'] = pd.to_datetime(arquivo['data_transacao'], errors='coerce')
    
    return arquivo


def listar_investimentos():
    tabela = [f"{'Moeda':^5} | {'Transação':^9} | {'Data da Transacao':^15} | {'Cotação na Data':^18} | {'Comprado':^12} | {'Total Comprado':^14} | {'Cotação Atual':^15}"]
    arquivo = ler_arquivo_investimentos()
    
    for i, row in arquivo.iterrows():
        cotacacao = float(cotar_moeda(row['moeda']))
        data_formatada = row['data_transacao'].strftime('%d/%m/%Y') if pd.notnull(row['data_transacao']) else 'N/A'
        
        tabela.append(f"{row['moeda']:^5} | {row['transacao']:^9} | {data_formatada:^17} | R${row['cotacao_na_data']:^16} | R${row['comprado']:^10.2f} | {row['total_comprado']:^14.10f} | {cotacacao:^15.10f}")
        
    return tabela
        

def somar_investimentos():
    arquivo = ler_arquivo_investimentos()
    soma = 0
    for i, row in arquivo.iterrows():
        soma+= float(row['comprado'])
        
    return soma
