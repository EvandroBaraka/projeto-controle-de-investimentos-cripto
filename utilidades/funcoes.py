import pandas as pd
import requests
import os
import tkinter
from tkinter import messagebox


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
    

def formatar_cotacao(moeda_selecionada):
    valor = float(cotar_moeda(moeda_selecionada))
    if(valor >= 0.10):
        return f'R$ {valor:.2f}'
    else:
        return f'R$ {valor:.8f}'


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


def obter_cotacao_historica(moeda_cotada, data, intervalo='1d', moeda_base='BRL'):
    """
    Obtém a cotação histórica de uma criptomoeda em uma data específica.
    
    Args:
        moeda_base (str): Moeda base (padrão: 'BRL').
        moeda_cotada (str): Moeda de cotação (exemplo: 'BTC').
        data (str): Data no formato 'YYYY-MM-DD'.
        intervalo (str): Intervalo de tempo (padrão: '1d' para diário).
        
    Returns:
        Cotação média na data selecionada.
    """
    from datetime import datetime
    
    # Converte a data para timestamp em milissegundos
    timestamp = int(datetime.strptime(str(data), "%Y-%m-%d").timestamp() * 1000)
    
    # Par de moedas
    symbol = f"{moeda_cotada}{moeda_base}".upper()
    
    # Endpoint da Binance
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": intervalo,
        "startTime": timestamp,
        "limit": 1
    }
    
    try:
        # Faz a requisição
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data:
            # Desestrutura os dados do candlestick
            candle = data[0]
            media_na_data = (float(candle[2]) + float(candle[3])) / 2
            # return {
            #     "abertura": float(candle[1]),
            #     "fechamento": float(candle[4]),
            #     "máxima": float(candle[2]),
            #     "mínima": float(candle[3]),
            #     "volume": float(candle[5]),
            #     "data": datetime.fromtimestamp(candle[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            # }
            return media_na_data
        else:
            return {"erro": "Nenhum dado encontrado para a data fornecida."}
    except Exception as e:
        return {"erro": str(e)}


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


def adicionar_investimento_no_arquivo(moeda, dataTransacao, cotacao, valor, total, transacao='compra', posicao='len(arquivo)'):
    arquivo = ler_arquivo_investimentos()
    novaLinha = [moeda, transacao, dataTransacao, cotacao, valor, total]
    
    novaLinha[2] = pd.to_datetime(novaLinha[2], errors='coerce')
    
    arquivo.loc[posicao] = novaLinha
    
    arquivo.to_excel('utilidades/compra_cripto.xlsx', index=False)
    print('Dados adicionados.')
        

def somar_investimentos():
    arquivo = ler_arquivo_investimentos()
    soma = 0
    for i, row in arquivo.iterrows():
        soma+= float(row['comprado'])
        
    return soma


def total_lucro_atual():
    arquivo = ler_arquivo_investimentos()
    total = 0
    for i, row in arquivo.iterrows():
        cotacao = float(cotar_moeda(row['moeda']))
        total += row['total_comprado'] * cotacao
    
    return total


def deletar_dados(treeview):
    try:
        arquivo = ler_arquivo_investimentos()
        item_selecionado = treeview.selection()[0]
        indice_item_selecionado = treeview.index(item_selecionado)
        valores = treeview.item(item_selecionado, 'values')
        linha_para_remover = arquivo[arquivo.index == indice_item_selecionado].index
        
        resposta = messagebox.askokcancel(title='Confirmar remoção de dados', message=f'Deseja realmente remover os dados:\n{valores}')
        
        if(resposta):
            arquivo.drop(linha_para_remover, axis=0, inplace=True)
            arquivo.to_excel('utilidades/compra_cripto.xlsx', index=False)
            treeview.delete(item_selecionado)
    
    except:
        tkinter.messagebox.showinfo(title='ERRO', message=f'Selecione o item a ser deletado.')
