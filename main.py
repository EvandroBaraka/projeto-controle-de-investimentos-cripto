import customtkinter as tk
from utilidades.funcoes import *
from utilidades.registro_compra import *


def atualizar_tabela():
    tabela_investimentos = listar_investimentos()
    tabela_em_string = ''
    for linha in tabela_investimentos:
        tabela_em_string += linha + '\n'
        
    janela_dados_investimentos.configure(state='normal')
    
    janela_dados_investimentos.delete(0.0, 'end')
    janela_dados_investimentos.insert(0.0, tabela_em_string)
    
    janela_dados_investimentos.configure(state='disable')
        
    return tabela_em_string


def exibir_soma_investimentos():
    soma = somar_investimentos()
    label_total_investido.configure(text=f'Total investido\nR$ {soma:.2f}')
    

def exibir_total_lucro():
    soma_investido = somar_investimentos()
    soma_atual = total_lucro_atual()
    total = soma_atual - soma_investido
    
    if total > 0:
        valor_lucro_prejuizo.configure(text_color='green', font=('', 18), text=f'R$ {total:.2f}')
    else:
        valor_lucro_prejuizo.configure(text_color='red', font=('', 18), text=f'R$ {total:.2f}')
        

def configurar_label_cotacao(valor):
    valor_moeda.configure(text=valor)
    

janela = tk.CTk()
janela.geometry('650x560')
janela.title('Controle de Criptos')
janela.grid_columnconfigure((0, 1), weight=1)

lista_criptos = nomes_moedas()    
    
# Criar labels e campos
titulo = tk.CTkLabel(janela, font=('', 24), text='Controle de Criptos')
label_consulta = tk.CTkLabel(janela, font=('', 18), text='Consulta Cripto')
label_cotacao = tk.CTkLabel(janela, font=('', 18), text='Cotação Atual')

select_moeda = tk.CTkOptionMenu(janela, width=200, font=('', 16), values=lista_criptos, command=lambda moeda: configurar_label_cotacao(formatar_cotacao(moeda)))

valor_moeda = tk.CTkLabel(janela, font=('', 16), text='R$ 0,00')
label_compra = tk.CTkLabel(janela, font=('', 18), text='Compra de Moeda')
campo_compra = tk.CTkEntry(janela, width=170, placeholder_text='Digite o Valor comprado')
botao_comprar = tk.CTkButton(janela, height=50, border_width=3, hover=True, font=('', 16), text='Comprar', 
                             command=lambda: abrir_janela_registro_compra(janela, select_moeda.get(), campo_compra.get()))
janela_dados_investimentos = tk.CTkTextbox(janela, wrap='none', font=('Courier New', 13), width=730, height=200)
frame_total_investido = tk.CTkFrame(janela)
label_total_investido = tk.CTkLabel(frame_total_investido)
frame_lucro_prejuizo = tk.CTkFrame(janela)
label_lucro_prejuizo = tk.CTkLabel(frame_lucro_prejuizo, text='Lucro/Prejuízo Total')
valor_lucro_prejuizo = tk.CTkLabel(frame_lucro_prejuizo)


# Posicionar na janela
titulo.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
label_consulta.grid(column=0, row=1, pady=(0, 10), padx=20, sticky='w')
label_cotacao.grid(column=1, row=1, pady=(0, 10), padx=20, sticky='w')
select_moeda.grid(column=0, row=2, pady=(0, 10), padx=20, sticky='w')
valor_moeda.grid(column=1, row=2, pady=(0, 10), padx=20, sticky='w')
label_compra.grid(column=0, row=4, pady=(20, 10), padx=20, sticky='w')
campo_compra.grid(column=0, row=5, pady=(0, 10), padx=20, sticky='w')
botao_comprar.grid(column=1, row=4, pady=(0, 10), padx=20, sticky='sew', rowspan=2)
janela_dados_investimentos.grid(column=0, row=6, pady=20, padx=10, columnspan=2)
frame_total_investido.grid(column=0, row=7, pady=(0,20), padx=20, columnspan=2, sticky='w')
label_total_investido.pack(pady=10, padx=40)
frame_lucro_prejuizo.grid(column=1, row=7, pady=(0,20), padx=20)
label_lucro_prejuizo.pack(padx=30)
valor_lucro_prejuizo.pack()



atualizar_tabela()
exibir_soma_investimentos()
exibir_total_lucro()


janela.mainloop()