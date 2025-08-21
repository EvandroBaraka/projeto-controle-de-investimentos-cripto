import pandas as pd
import requests
from requests.exceptions import RequestException, ConnectionError, SSLError
import time
import os
import tkinter
from tkinter import messagebox


def nomes_moedas():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    retries = 2 # Número de tentativas
    delay = 5 # Tempo de espera entre as tentativas (em segundos)
    
    for i in range(retries):
        try:
            resposta = requests.get(url, timeout=10) # Adiciona um timeout
            resposta.raise_for_status() # Lança um erro para códigos de status HTTP ruins
            
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
        except (RequestException, ConnectionError, SSLError) as e:
            # Captura erros de requisição, conexão e SSL
            print(f"Erro na tentativa {i+1} de conectar à API: {e}")
            if i < retries - 1:
                print(f"Tentando novamente em {delay} segundos...")
                time.sleep(delay)
            else:
                print("Todas as tentativas falharam. Verifique sua conexão ou firewall.")
                return [] # Retorna uma lista vazia para evitar quebra do programa
        except Exception as e:
            # Captura outros erros inesperados
            print(f"Ocorreu um erro inesperado: {e}")
            return [] # Retorna uma lista vazia para evitar quebra do programa
            
    return []
    

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
        retries = 2
        delay = 5
        
        for i in range(retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                preco = response.json()
                return preco['price']
            
            except (RequestException, ConnectionError, SSLError) as e:
                print(f"Erro na tentativa {i+1} de cotar {moeda}: {e}")
                if i < retries - 1:
                    print(f"Tentando novamente em {delay} segundos...")
                    time.sleep(delay)
                else:
                    print(f"Todas as tentativas de cotar {moeda} falharam. Verifique sua conexão ou firewall.")
                    return 0.0
                
            except Exception as e:
                print(f"Ocorreu um erro inesperado ao cotar {moeda}: {e}")
                return 0.0
    
    else:
        return 0.0


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


def listar_dados_carteira():
    """
    Função que busca os dados no arquivo de investimentos e transforma em uma lista com os dados de carteira atual

    Returns:
        list: lista com as colunas moeda, quantidade total, cotação atual, total investido, valor atual total, lucro/prejuizo, % lucro/preejuizo
    """
    try:
        arquivo = ler_arquivo_investimentos()
        
        dadosCarteira = {
            'cripto': [],
            'quantidade': [],
            'total_investido': []
        }
        for i, row in arquivo.iterrows():
            if(row['moeda'] not in dadosCarteira['cripto']):
                dadosCarteira['cripto'].append(row['moeda'])
                dadosCarteira['quantidade'].append(row['total_comprado'])
                dadosCarteira['total_investido'].append(row['comprado'])
            else:
                if(row['transacao'] == 'compra'):
                    dadosCarteira['quantidade'][dadosCarteira['cripto'].index(row['moeda'])] += row['total_comprado']
                    dadosCarteira['total_investido'][dadosCarteira['cripto'].index(row['moeda'])] += row['comprado']
                    
                elif(row['transacao'] == 'venda'):
                    dadosCarteira['quantidade'][dadosCarteira['cripto'].index(row['moeda'])] -= row['total_comprado']
                    dadosCarteira['total_investido'][dadosCarteira['cripto'].index(row['moeda'])] -= row['comprado']
        
        lista = []
        for i in range(0, len(dadosCarteira['cripto'])):
            if(dadosCarteira['quantidade'][i] > 0):
                cripto = dadosCarteira['cripto'][i]
                qtd_total = dadosCarteira['quantidade'][i]
                total_investido = dadosCarteira['total_investido'][i]
                cotacao_atual = cotar_moeda(dadosCarteira['cripto'][i])
                valor_atual_total = float(qtd_total) * float(cotacao_atual)
                lucro_prejuizo = valor_atual_total - total_investido
                porcentagem_lucro_prejuizo = (lucro_prejuizo / total_investido) * 100
                
                nova_linha = [cripto, qtd_total, cotacao_atual, f'R$ {total_investido:.2f}', f'R$ {valor_atual_total:.2f}', f'R$ {lucro_prejuizo:.2f}', f'{porcentagem_lucro_prejuizo:.2f}%']
                lista.append(nova_linha)
                
        return lista
    
    except Exception as e:
        print(f'Erro ao trazer dados da carteira: {e}')
        raise
        
        
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
        if(row['transacao'] == 'compra'):
            soma += float(row['comprado'])
            
        elif(row['transacao'] == 'venda'):
            soma -= float(row['comprado'])
        
    return soma


def total_lucro_atual():
    arquivo = ler_arquivo_investimentos()
    total = 0
    for i, row in arquivo.iterrows():
        cotacao = float(cotar_moeda(row['moeda']))
        if(row['transacao'] == 'compra'):
            total += row['total_comprado'] * cotacao
        elif(row['transacao'] == 'venda'):
            total -= row['total_comprado'] * cotacao
    
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
