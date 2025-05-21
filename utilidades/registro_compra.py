import customtkinter as tk
from utilidades.funcoes import *
from tkcalendar import DateEntry


def calcula_total_comprado(valorComprado, cotacao):
    if(valorComprado == ''):
        valorComprado = '0'
    if(cotacao == ''):
        cotacao = '0'
    
    valorComprado = valorComprado.replace(',', '.').replace('r', '').replace('R', '').replace('$', '').replace(':', '').replace('=', '').strip()
    cotacao = cotacao.replace(',', '.').replace('r', '').replace('R', '').replace('$', '').replace(':', '').replace('=', '').strip()
    
    try:
        resultado = float(valorComprado) / float(cotacao)
        
    except Exception as e:
        print(f'Erro: {e}')
        resultado = 0
        
    return resultado


def abrir_janela_registro_compra(janela_pai, moeda_selecionada='Selecione a moeda', valor_comprado=0):
    
    def ajustar_campo_cotacao(moeda):
        cotacao = formatar_cotacao(moeda)
        campo_cotacao.configure(state='normal')
        campo_cotacao.delete(first_index=0, last_index=99)
        campo_cotacao.insert(0, cotacao)
        campo_cotacao.configure(state='disable')
    
    
    def ajustar_campo_total_comprado(event=None):
        totalComprado = calcula_total_comprado(campo_valor_comprado.get(), campo_cotacao.get())
        campo_total_comprado.configure(state='normal')
        campo_total_comprado.delete(first_index=0, last_index=99)
        campo_total_comprado.insert(0, totalComprado)
        campo_total_comprado.configure(state='disable')
        
        
    def on_nova_cripto_selecionada(moeda):
        ajustar_campo_cotacao(moeda)
        ajustar_campo_total_comprado()
    
    
    janelaRegistroCompra = tk.CTkToplevel(janela_pai)
    janelaRegistroCompra.title('Registro de Compra')
    janelaRegistroCompra.geometry('400x600')
    janelaRegistroCompra.lift()
    janelaRegistroCompra.focus_force()
    janelaRegistroCompra.grab_set()
    
    if(moeda_selecionada != 'Selecione a moeda'):
        cotacao = cotar_moeda(moeda_selecionada)
    else:
        cotacao = 0
    lista_criptos = nomes_moedas()
    
    label_moeda = tk.CTkLabel(janelaRegistroCompra, font=('', 18), text='Moeda Comprada')
    campo_select_moeda = tk.CTkOptionMenu(janelaRegistroCompra, width=200, font=('', 16), values=lista_criptos, command=lambda moeda: on_nova_cripto_selecionada(moeda))
    campo_select_moeda.set(moeda_selecionada)
    
    label_data_transacao = tk.CTkLabel(janelaRegistroCompra, font=('', 18), text='Data da Transação')
    campo_data = DateEntry(janelaRegistroCompra, date_pattern="dd/mm/yyyy", background="darkblue", foreground="darkblue", borderwidth=2, font=('', 15))
    
    label_cotacao = tk.CTkLabel(janelaRegistroCompra, font=('', 18), text='Cotação na data')
    campo_cotacao = tk.CTkEntry(janelaRegistroCompra, width=170)
    campo_cotacao.insert(0, cotacao)
    campo_cotacao.configure(state='disable')
    
    label_valor_comprado = tk.CTkLabel(janelaRegistroCompra, font=('', 18), text='Valor comprado em R$')
    campo_valor_comprado = tk.CTkEntry(janelaRegistroCompra, width=170)
    campo_valor_comprado.insert(0, valor_comprado)
    
    label_total_comprado = tk.CTkLabel(janelaRegistroCompra, font=('', 18), text='Tota comprado')
    campo_total_comprado = tk.CTkEntry(janelaRegistroCompra, width=170)
    
    campo_valor_comprado.bind("<FocusOut>", lambda event: ajustar_campo_total_comprado())
    campo_valor_comprado.bind("<KeyRelease>", lambda event: ajustar_campo_total_comprado())
    
    botao_registrar_compra = tk.CTkButton(janelaRegistroCompra, height=50, border_width=3, hover=True, font=('', 16), text='Registrar Compra', command=lambda:(print('registrado')))
    
    
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
    
    ajustar_campo_total_comprado()