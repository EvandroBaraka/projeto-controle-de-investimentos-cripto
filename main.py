import tkinter
from tkinter import ttk
import customtkinter as tk
import threading
from utilidades.funcoes import *
from utilidades.registro_compra import *


def atualizar_dados_em_thread(popup, progress_bar):
    """
    Função executada em uma thread separada para atualizar os dados.

    Parâmetros:
        popup (tk.CTkToplevel): A janela popup de progresso.
        progress_bar (tk.CTkProgressBar): A barra de progresso na popup.
    """
    print('Atualizando dados (em thread)... INÍCIO')
    total_etapas = 3
    for i in range(total_etapas):
        if i == 0:
            print('Atualizando tabela...')
            try:
                atualizar_tabela()
                print('Tabela atualizada.')
            except Exception as e:
                print(f"Erro ao atualizar tabela: {e}")
                janela.after(0, lambda: mostrar_erro(popup, "Erro ao atualizar tabela."))
                return # Encerra a thread
        elif i == 1:
            print('Exibindo soma dos investimentos...')
            try:
                exibir_soma_investimentos()
                print('Soma dos investimentos exibida.')
            except Exception as e:
                print(f"Erro ao exibir soma: {e}")
                janela.after(0, lambda: mostrar_erro(popup, "Erro ao exibir soma dos investimentos."))
                return # Encerra a thread
        elif i == 2:
            print('Exibindo lucro total...')
            try:
                exibir_total_lucro()
                print('Lucro total exibido.')
            except Exception as e:
                print(f"Erro ao exibir lucro: {e}")
                janela.after(0, lambda: mostrar_erro(popup, "Erro ao exibir lucro total."))
                return # Encerra a thread
        progress_bar.set((i + 1) / total_etapas)  # Atualiza a barra de progresso
    print('Dados atualizados (em thread)! FIM')
    janela.after(0, popup.destroy)


def mostrar_erro(parent, mensagem):
    """
    Função para exibir uma mensagem de erro em uma popup.

    Parâmetros:
        parent (tk.CTk): Janela pai.
        mensagem (str): Mensagem de erro a exibir.
    """
    erro_popup = tk.CTkToplevel(parent)
    erro_popup.title("Erro")
    erro_popup.grab_set()
    tk.CTkLabel(erro_popup, text=mensagem).pack(padx=20, pady=10)
    tk.CTkButton(erro_popup, text="OK", command=erro_popup.destroy).pack(padx=20, pady=10)


def atualizar_todos_dados():
    """
    Função chamada ao clicar no botão de atualizar.
    Cria a popup de progresso e inicia a thread de atualização.
    """
    popup = tk.CTkToplevel(janela)
    popup.title('Atualizando Valores...')
    popup.geometry('200x100')
    popup.grab_set()
    label = tk.CTkLabel(popup, text="Atualizando Valores...")
    label.pack(padx=20, pady=10)
    progress_bar = tk.CTkProgressBar(popup, mode='determinate')
    progress_bar.pack(padx=20, pady=10)
    progress_bar.set(0)

    thread_atualizacao = threading.Thread(target=atualizar_dados_em_thread, args=(popup, progress_bar))
    thread_atualizacao.start()
    botao_atualizar_tabela.configure(state="disabled")  # Desabilita o botão durante a atualização
    janela.after(10, verificar_thread_e_reabilitar_botao, thread_atualizacao)  # Inicia a verificação


def verificar_thread_e_reabilitar_botao(thread):
    """
    Função para verificar se a thread de atualização terminou e reabilitar o botão.

    Parâmetros:
        thread (threading.Thread): A thread de atualização.
    """
    if thread.is_alive():
        janela.after(10, verificar_thread_e_reabilitar_botao, thread)  # Verifica novamente após 10ms
    else:
        botao_atualizar_tabela.configure(state="normal")  # Reabilita o botão após a conclusão


def atualizar_tabela():
    """
    Função para atualizar a tabela de investimentos na interface.
    """
    try:
        tabelaInvestimentos = ler_arquivo_investimentos()
        
        for item in tabela_dados_investimentos.get_children():
            tabela_dados_investimentos.delete(item)
            
        for i, row in tabelaInvestimentos.iterrows():
            cotacaoAtual = float(cotar_moeda(row['moeda']))
            dataFormatada = row['data_transacao'].strftime('%d/%m/%Y') if pd.notnull(row['data_transacao']) else 'N/A'
            novaLinha = [row['moeda'], row['transacao'], dataFormatada, row['cotacao_na_data'], row['comprado'], row['total_comprado'], cotacaoAtual]
            
            tabela_dados_investimentos.insert('', tkinter.END, values=novaLinha)
    except Exception as e:
        print(f'Erro ao atualizar a tabela: {e}')
        raise # Re-lança a exceção para ser tratada na thread
    

def exibir_soma_investimentos():
    """
    Função para exibir a soma dos investimentos.
    """
    try:
        soma = somar_investimentos()
        label_total_investido.configure(text=f'Total investido\nR$ {soma:.2f}')
    except Exception as e:
        print(f"Erro ao exibir soma dos investimentos: {e}")
        raise  # Re-lança a exceção para ser tratada na thread


def exibir_total_lucro():
    """
    Função para exibir o lucro total.
    """
    try:
        soma_investido = somar_investimentos()
        soma_atual = total_lucro_atual()
        total = soma_atual - soma_investido

        if total > 0:
            valor_lucro_prejuizo.configure(text_color='green', font=('', 18), text=f'R$ {total:.2f}')
        else:
            valor_lucro_prejuizo.configure(text_color='red', font=('', 18), text=f'R$ {total:.2f}')
    except Exception as e:
        print(f"Erro ao exibir lucro total: {e}")
        raise  # Re-lança a exceção para ser tratada na thread


def configurar_label_cotacao(valor):
    """
    Função para configurar o texto de um label com o valor da cotação.
    """
    valor_moeda.configure(text=valor)


janela = tk.CTk()
janela.geometry('700x680')
janela.title('Controle de Criptos')
janela.grid_columnconfigure((0, 1, 2), weight=1)

lista_criptos = nomes_moedas()

# Criar labels e campos
titulo = tk.CTkLabel(janela, font=('', 24), text='Controle de Criptos')
label_consulta = tk.CTkLabel(janela, font=('', 18), text='Consulta Cripto')
label_cotacao = tk.CTkLabel(janela, font=('', 18), text='Cotação Atual')

select_moeda = tk.CTkOptionMenu(janela, width=200, font=('', 16), values=lista_criptos,
                                command=lambda moeda: configurar_label_cotacao(formatar_cotacao(moeda)))

valor_moeda = tk.CTkLabel(janela, font=('', 16), text='R$ 0,00')
label_compra = tk.CTkLabel(janela, font=('', 18), text='Compra de Moeda')
campo_compra = tk.CTkEntry(janela, width=170, placeholder_text='Digite o Valor comprado')
botao_registrar = tk.CTkButton(janela, height=50, border_width=3, hover=True, font=('', 16), text='Novo Registro', 
                             command=lambda: abrir_janela_registro_compra(janela, select_moeda.get(), campo_compra.get()))

tabview = tk.CTkTabview(janela)
tabview.add("Histórico de Transações")
tabview.add("Carteira Atual")
tabview.set("Histórico de Transações")

style = ttk.Style()
style.configure('Treeview.Heading', font=('', 11, 'bold'))
style.configure('Treeview', font=('', 10))

tabela_dados_investimentos = ttk.Treeview(tabview.tab('Histórico de Transações'), columns=['column1', 'column2', 'column3', 'column4', 'column5', 'column6', 'column7'], show='headings')
tabela_dados_investimentos.column('column1', width=60, minwidth=60, stretch=False)
tabela_dados_investimentos.heading('#1', text='Moeda', anchor='center')
tabela_dados_investimentos.column('column2', width=90, minwidth=50, stretch=False)
tabela_dados_investimentos.heading('#2', text='Transação', anchor='center')
tabela_dados_investimentos.column('column3', width=75, minwidth=50, stretch=False)
tabela_dados_investimentos.heading('#3', text='Data', anchor='center')
tabela_dados_investimentos.column('column4', width=90, minwidth=50, stretch=False)
tabela_dados_investimentos.heading('#4', text='Cotação')
tabela_dados_investimentos.column('column5', width=120, minwidth=50, stretch=False)
tabela_dados_investimentos.heading('#5', text='Valor Comprado')
tabela_dados_investimentos.column('column6', width=130, minwidth=50, stretch=False)
tabela_dados_investimentos.heading('#6', text='Total Comprado')
tabela_dados_investimentos.column('column7', width=120, minwidth=50, stretch=False)
tabela_dados_investimentos.heading('#7', text='Cotação Atual')
tabela_dados_investimentos.pack()

tabela_carteira_atual = ttk.Treeview(tabview.tab('Carteira Atual'), columns=['column1', 'column2', 'column3', 'column4', 'column5', 'column6', 'column7'], show='headings')
tabela_carteira_atual.column('column1', width=60, minwidth=60, stretch=False)
tabela_carteira_atual.heading('#1', text='Cripto', anchor='center')
tabela_carteira_atual.column('column2', width=90, minwidth=50, stretch=False)
tabela_carteira_atual.heading('#2', text='Quant. Total', anchor='center')
tabela_carteira_atual.column('column3', width=75, minwidth=50, stretch=False)
tabela_carteira_atual.heading('#3', text='Custo Médio', anchor='center')
tabela_carteira_atual.column('column4', width=90, minwidth=50, stretch=False)
tabela_carteira_atual.heading('#4', text='Cotação Atual')
tabela_carteira_atual.column('column5', width=120, minwidth=50, stretch=False)
tabela_carteira_atual.heading('#5', text='Valor Atual Total')
tabela_carteira_atual.column('column6', width=130, minwidth=50, stretch=False)
tabela_carteira_atual.heading('#6', text='Lucro/Prejuízo')
tabela_carteira_atual.column('column7', width=120, minwidth=50, stretch=False)
tabela_carteira_atual.heading('#7', text='% Lucro/Prejuízo')
tabela_carteira_atual.pack()

botao_deletar = tk.CTkButton(janela, hover=True, text='Deletar', command=lambda: deletar_dados(tabela_dados_investimentos))

frame_total_investido = tk.CTkFrame(janela)
label_total_investido = tk.CTkLabel(frame_total_investido)
frame_lucro_prejuizo = tk.CTkFrame(janela)
label_lucro_prejuizo = tk.CTkLabel(frame_lucro_prejuizo, text='Lucro/Prejuízo Total')
valor_lucro_prejuizo = tk.CTkLabel(frame_lucro_prejuizo)
botao_atualizar_tabela = tk.CTkButton(janela, height=50, border_width=2, hover=True, text='Atualizar Tabela',
                                     command=atualizar_todos_dados)

# Posicionar na janela
titulo.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=3)
label_consulta.grid(column=0, row=1, pady=(0, 10), padx=20, sticky='w', columnspan=2)
label_cotacao.grid(column=2, row=1, pady=(0, 10), padx=20, sticky='w', columnspan=2)
select_moeda.grid(column=0, row=2, pady=(0, 10), padx=20, sticky='w', columnspan=2)
valor_moeda.grid(column=2, row=2, pady=(0, 10), padx=20, sticky='w', columnspan=2)
label_compra.grid(column=0, row=4, pady=(20, 10), padx=20, sticky='w', columnspan=2)
campo_compra.grid(column=0, row=5, pady=(0, 10), padx=20, sticky='w', columnspan=2)
botao_registrar.grid(column=2, row=4, pady=(0, 10), padx=20, sticky='sew', rowspan=2, columnspan=2)
tabview.grid(column=0, row=6, pady=20, padx=10, columnspan=3)
botao_deletar.grid(column=1, row=7, pady=(0, 20))
frame_total_investido.grid(column=0, row=8, pady=(0, 20), padx=20, sticky='w')
label_total_investido.pack(pady=10, padx=40)
frame_lucro_prejuizo.grid(column=2, row=8, pady=(0, 20), padx=20)
label_lucro_prejuizo.pack(padx=30)
valor_lucro_prejuizo.pack()
botao_atualizar_tabela.grid(column=1, row=8, pady=(0, 20), sticky='ew')

# Chamadas iniciais para exibir os dados
atualizar_tabela()
exibir_soma_investimentos()
exibir_total_lucro()

janela.mainloop()