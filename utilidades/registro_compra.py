from tkinter import messagebox
import customtkinter as tk
from utilidades.funcoes import *
from tkcalendar import DateEntry


def calcula_total(transacao, valor, cotacao):
    if(valor == ''):
        valor = '0'
    if(cotacao == ''):
        cotacao = '0'
    
    valor = valor.replace(',', '.').replace('r', '').replace('R', '').replace('$', '').replace(':', '').replace('=', '').strip()
    cotacao = cotacao.replace(',', '.').replace('r', '').replace('R', '').replace('$', '').replace(':', '').replace('=', '').strip()
    
    try:
        if(transacao == 'compra'):
            resultado = float(valor) / float(cotacao)
            
        elif(transacao == 'venda'):
            resultado = float(valor) * float(cotacao)
        
    except Exception as e:
        print(f'Erro: {e}')
        resultado = 0
        return resultado
        
    if(float(cotacao) > 10000):
        return f'{resultado:.12f}'
    else:
        return resultado


def abrir_janela_registro_compra(janela_pai, moeda_selecionada='Selecione a moeda', valor_comprado=0):
    
    def ajustar_campo_cotacao(campoCotacao, cotacao):
        campoCotacao.configure(state='normal')
        campoCotacao.delete(first_index=0, last_index=99)
        campoCotacao.insert(0, cotacao)
        campoCotacao.configure(state='disable')
    
    
    def on_data_alterada(transacao, moeda, data, campoData, campoCotacao, campoValor, campoTotal, event=None):
        from datetime import date
        
        if(moeda.upper() == 'SELECIONE A MOEDA'):
            messagebox.showerror(title='Selecione uma moeda', message='Selecione uma moeda para consultar a cotação.')
            campoData.set_date(date.today())
            return
        if(data > date.today()):
            messagebox.showerror(title='Data inválida', message='Selecione uma data válida.\nDatas futuras não são aceitas')
            campoData.set_date(date.today())
            return
        try:
            cotacao_media_na_data = obter_cotacao_historica(moeda, data)
            ajustar_campo_cotacao(campoCotacao, cotacao_media_na_data)
            ajustar_campo_total(transacao, campoValor, campoCotacao, campoTotal)
        
        except Exception as e:
            messagebox.showerror(title='Erro', message=f'Erro: {e}')
        
        
    def ajustar_campo_total(transacao, campoValor, campoCotacao, campoTotal, event=None):
        totalComprado = calcula_total(transacao, campoValor.get(), campoCotacao.get())
        campoTotal.configure(state='normal')
        campoTotal.delete(first_index=0, last_index=99)
        campoTotal.insert(0, str(totalComprado))
        campoTotal.configure(state='disable')
        
        
    def on_nova_cripto_selecionada(transacao, moeda, campoCotacao, campoValor, campoTotal):
        if(moeda.upper() == 'SELECIONE A MOEDA'):
            return
        cotacao = formatar_cotacao(moeda)
        ajustar_campo_cotacao(campoCotacao, cotacao)
        ajustar_campo_total(transacao, campoValor, campoCotacao, campoTotal)
    
    
    def registrar_compra(transacao, moeda, data, cotacao, valor, total):
        adicionar_investimento_no_arquivo(moeda, data, cotacao.replace('R$', ''), valor, total, transacao)
        janelaRegistroCompra.destroy()
    
    
    def confirmar_registro(transacao, moeda, data, cotacao, valor, total):
        print('Confirmação...')
        
        if(transacao == 'compra'):
            strDadosCompra = f'Tipo de transação: {transacao}\n\nMoeda: {moeda} \n\nData: {data}\n\nCotação: {cotacao}\n\nValor comprado: R${float(valor):.2f}\n\nTotal Comprado: {moeda} {total}'
        
        elif(transacao == 'venda'):
            strDadosCompra = f'Tipo de transação: {transacao}\n\nCripto: {moeda} \n\nData: {data}\n\nCotação: {cotacao}\n\nQuantidade a vender: {moeda} {valor}\n\nValor Recebido: R$ {float(total):.2f}'
        
        resposta = messagebox.askokcancel(title='Confirmar Registro', message=f'Confirme os dados e pressione OK:\n{strDadosCompra}')
        
        if(resposta):
            registrar_compra(transacao, moeda, data, cotacao, valor, total)
        
    
    janelaRegistroCompra = tk.CTkToplevel(janela_pai)
    janelaRegistroCompra.title('Registro de Compra')
    janelaRegistroCompra.geometry('400x600')
    janelaRegistroCompra.grab_set()
    
    tabview = tk.CTkTabview(janelaRegistroCompra)
    tabview.add('Compra')
    tabview.add('Venda')
    tabview.set('Compra')
    
    if(moeda_selecionada != 'Selecione a moeda'):
        cotacao = cotar_moeda(moeda_selecionada)
    else:
        cotacao = 0
    lista_criptos = nomes_moedas()
    
    # Campos da tela de Compra
    label_moeda = tk.CTkLabel(tabview.tab('Compra'), font=('', 18), text='Moeda Comprada')
    campo_select_moeda = tk.CTkOptionMenu(tabview.tab('Compra'), width=200, font=('', 16), values=lista_criptos, command=lambda moeda: on_nova_cripto_selecionada('compra', moeda, campo_cotacao, campo_valor_comprado, campo_total_comprado))
    campo_select_moeda.set(moeda_selecionada)
    
    label_data_transacao = tk.CTkLabel(tabview.tab('Compra'), font=('', 18), text='Data da Transação')
    campo_data = DateEntry(tabview.tab('Compra'), date_pattern="dd/mm/yyyy", borderwidth=2, font=('', 13))
    
    label_cotacao = tk.CTkLabel(tabview.tab('Compra'), font=('', 18), text='Cotação na data')
    campo_cotacao = tk.CTkEntry(tabview.tab('Compra'), width=170)
    campo_cotacao.insert(0, cotacao)
    campo_cotacao.configure(state='disable')
    
    label_valor_comprado = tk.CTkLabel(tabview.tab('Compra'), font=('', 18), text='Valor comprado em R$')
    campo_valor_comprado = tk.CTkEntry(tabview.tab('Compra'), width=170)
    campo_valor_comprado.insert(0, valor_comprado)
    
    label_total_comprado = tk.CTkLabel(tabview.tab('Compra'), font=('', 18), text='Tota comprado')
    campo_total_comprado = tk.CTkEntry(tabview.tab('Compra'), width=170)
    
    campo_data.bind('<<DateEntrySelected>>', lambda event: on_data_alterada('compra', campo_select_moeda.get(), campo_data.get_date(), campo_data, campo_cotacao, campo_valor_comprado, campo_total_comprado))
    campo_valor_comprado.bind("<FocusOut>", lambda event: ajustar_campo_total('compra', campo_valor_comprado, campo_cotacao, campo_total_comprado))
    campo_valor_comprado.bind("<KeyRelease>", lambda event: ajustar_campo_total('compra', campo_valor_comprado, campo_cotacao, campo_total_comprado))
    
    botao_registrar_compra = tk.CTkButton(tabview.tab('Compra'), height=50, border_width=3, hover=True, font=('', 16), text='Registrar Compra', command=lambda: confirmar_registro(
                                        transacao='compra', 
                                        moeda=campo_select_moeda.get(), 
                                        data=campo_data.get_date(), 
                                        cotacao=campo_cotacao.get(), 
                                        valor=campo_valor_comprado.get(), 
                                        total=campo_total_comprado.get()))
    
    # Campos da tela de venda
    label_cripto = tk.CTkLabel(tabview.tab('Venda'), font=('', 18), text='Cripto')
    campo_select_cripto = tk.CTkOptionMenu(tabview.tab('Venda'), width=200, font=('', 16), values=lista_criptos, command=lambda moeda: on_nova_cripto_selecionada('venda', moeda, campo_cotacao_venda, campo_valor_vendido, campo_total_vendido))
    campo_select_cripto.set(moeda_selecionada)
    
    label_data_venda = tk.CTkLabel(tabview.tab('Venda'), font=('', 18), text='Data da Venda')
    campo_data_venda = DateEntry(tabview.tab('Venda'), date_pattern="dd/mm/yyyy", borderwidth=2, font=('', 13))
    
    label_cotacao_venda = tk.CTkLabel(tabview.tab('Venda'), font=('', 18), text='Cotação na data')
    campo_cotacao_venda = tk.CTkEntry(tabview.tab('Venda'), width=170)
    campo_cotacao_venda.insert(0, cotacao)
    campo_cotacao_venda.configure(state='disable')
    
    label_valor_vendido = tk.CTkLabel(tabview.tab('Venda'), font=('', 18), text='Quantidade a Vender')
    campo_valor_vendido = tk.CTkEntry(tabview.tab('Venda'), width=170)
    campo_valor_vendido.insert(0, valor_comprado)
    
    label_total_vendido = tk.CTkLabel(tabview.tab('Venda'), font=('', 18), text='Valor Recebido R$')
    campo_total_vendido = tk.CTkEntry(tabview.tab('Venda'), width=170)
    
    campo_data_venda.bind('<<DateEntrySelected>>', lambda event: on_data_alterada('venda', campo_select_cripto.get(), campo_data_venda.get_date(), campo_data_venda, campo_cotacao_venda, campo_valor_vendido, campo_total_vendido))
    campo_valor_vendido.bind("<FocusOut>", lambda event: ajustar_campo_total('venda', campo_valor_vendido, campo_cotacao_venda, campo_total_vendido))
    campo_valor_vendido.bind("<KeyRelease>", lambda event: ajustar_campo_total('venda', campo_valor_vendido, campo_cotacao_venda, campo_total_vendido))
    
    botao_registrar_venda = tk.CTkButton(tabview.tab('Venda'), height=50, border_width=3, hover=True, font=('', 16), text='Registrar Venda', command=lambda: confirmar_registro(
                                        transacao='venda',
                                        moeda=campo_select_cripto.get(),
                                        data=campo_data_venda.get_date(),
                                        cotacao=campo_cotacao_venda.get(),
                                        valor=campo_valor_vendido.get(),
                                        total=campo_total_vendido.get()))
    
    tabview.pack()
    # campos compra
    label_moeda.pack(pady=10)
    campo_select_moeda.pack(pady=(0, 20))
    label_data_transacao.pack(pady=10)
    campo_data.pack(pady=(0, 20))
    label_cotacao.pack(pady=10)
    campo_cotacao.pack(pady=(0, 20))
    label_valor_comprado.pack(pady=10)
    campo_valor_comprado.pack(pady=(0, 20))
    label_total_comprado.pack(pady=10)
    campo_total_comprado.pack(pady=(0, 20))
    botao_registrar_compra.pack(pady=10)
    
    #campos venda
    label_cripto.pack(pady=10)
    campo_select_cripto.pack(pady=(0, 20))
    label_data_venda.pack(pady=10)
    campo_data_venda.pack(pady=(0, 20))
    label_cotacao_venda.pack(pady=10)
    campo_cotacao_venda.pack(pady=(0, 20))
    label_valor_vendido.pack(pady=10)
    campo_valor_vendido.pack(pady=(0, 20))
    label_total_vendido.pack(pady=10)
    campo_total_vendido.pack(pady=(0, 20))
    botao_registrar_venda.pack(pady=10)
    
    ajustar_campo_total('compra', campo_valor_comprado, campo_cotacao, campo_total_comprado)
    ajustar_campo_total('venda', campo_valor_vendido, campo_cotacao_venda, campo_total_vendido)