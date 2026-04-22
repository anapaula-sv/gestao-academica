import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logica import calcular_situacao, validar_nota, max_notas
from database import db_listar_todos, db_cadastrar_aluno, db_buscar_aluno, db_atualizar_notas, db_excluir_aluno, db_cadastrar_usuario, db_verificar_usuario


def mostrar_texto(texto):
    resultado.config(state="normal")
    resultado.delete("1.0", tk.END)
    resultado.insert(tk.END, texto)
    resultado.config(state="disabled")

def atualizar_lista():
    lista_alunos.delete(0, tk.END)
    alunos_db = db_listar_todos()
    for aluno in alunos_db:
        lista_alunos.insert(tk.END, aluno["nome"])

def limpar_campos():
    entrada_nome.delete(0, tk.END)
    entrada_nota.delete(0, tk.END)
    
def atualizar_contador():
    alunos_db = db_listar_todos()
    total = len(alunos_db)
    total_label.config(text=f'{total} aluno(s) no sistema')


def cadastro_aluno():
    nome = entrada_nome.get().strip().title()

    if not nome:
        mostrar_texto("Digite um nome válido!")
        return

    if db_buscar_aluno(nome):
        mostrar_texto("Aluno já cadastrado!")
        return

    db_cadastrar_aluno(nome)

    limpar_campos()
    mostrar_texto(f"Aluno {nome} cadastrado com sucesso!")
    
    atualizar_contador()
    atualizar_lista()

def cadastro_nota():
    nome = entrada_nome.get().strip().title()

    if not nome:
        mostrar_texto("Digite o nome do aluno!")
        return

    nota, erro = validar_nota(entrada_nota.get())

    if erro:
        mostrar_texto(erro)
        return

    aluno = db_buscar_aluno(nome)

    if not aluno:
        mostrar_texto("Aluno não encontrado.")
        return

    if len(aluno['notas']) >= max_notas:
        mostrar_texto(f"{nome} já tem {max_notas} notas!")
        return

    aluno['notas'].append(nota)
    db_atualizar_notas(nome, aluno['notas'])

    media, situacao = calcular_situacao(aluno['notas'])
    restantes = max_notas - len(aluno['notas'])

    mostrar_texto(
        f"{nome}\n"
        f"Notas: {aluno['notas']}\n"
        f"Média: {media:.2f}\n"
        f"Situação: {situacao}\n"
        f"Faltam: {restantes} nota(s)"
    )
    limpar_campos()

def excluir_aluno():
    nome = entrada_nome.get().strip().title()

    if not nome:
        mostrar_texto('Digite o nome do aluno para excluir!')
        return

    aluno = db_buscar_aluno(nome)

    if not aluno:
        mostrar_texto('Aluno não encontrado!')
        return

    confirmacao = messagebox.askyesno("Confirmação", f"Deseja excluir {nome}?")

    if not confirmacao:
        return

    db_excluir_aluno(nome)
    atualizar_contador()
    atualizar_lista()
    limpar_campos()
    mostrar_texto(f'Aluno {nome} excluído com sucesso!')

def calcular_media():
    alunos_atuais = db_listar_todos() 
    
    if not alunos_atuais:
        mostrar_texto("Nenhum aluno cadastrado.")
        return

    texto = ""
    for aluno in alunos_atuais:
        if not aluno['notas']:
            texto += f'{aluno["nome"]} não tem notas cadastradas\n\n'
            continue

        media, situacao = calcular_situacao(aluno['notas'])
        texto += f'Nome: {aluno["nome"]}\n'
        texto += f'Notas: {aluno["notas"]}\n'
        texto += f'Média: {media:.2f}\n'
        texto += f'Situação: {situacao}\n'
        texto += "-" * 20 + "\n"

    mostrar_texto(texto)

def selecionar_aluno(event):
    selecao = lista_alunos.curselection()
    if selecao:
        nome_selecionado = lista_alunos.get(selecao[0])
        entrada_nome.delete(0, tk.END)
        entrada_nome.insert(0, nome_selecionado)
        
        aluno = db_buscar_aluno(nome_selecionado)
        if aluno:
            media, situacao = calcular_situacao(aluno['notas'])

            resumo = f"Aluno: {aluno['nome']}\n"
            resumo += f"Notas: {aluno['notas']}\n"
            resumo += f"Média: {media:.2f} | {situacao}"
            mostrar_texto(resumo)

CORES = {
    "fundo": "#1e1e1e",
    "entrada": "#333333",
    "btn_confirmar": "#941f1f",
    "btn_acao": "#ce6b5d",
    "btn_acao2": "#7b9971",
    "btn_acao3": "#34502b",
    "texto": "white"
}

janela = tk.Tk()
janela.title('Gestão Acadêmica')
janela.geometry('400x650')
janela.configure(bg=CORES["fundo"]) #


style = ttk.Style()
style.theme_use('default') 
style.configure("TFrame", background=CORES["fundo"])
style.configure("TLabel", background=CORES["fundo"], foreground=CORES["texto"], font=('Helvetica', 10))
style.configure("TLabelframe", background=CORES["fundo"], foreground=CORES["texto"])
style.configure("TLabelframe.Label", background=CORES["fundo"], foreground=CORES["texto"])


frame_input = ttk.Frame(janela, padding=20)
frame_input.pack(fill="x")

ttk.Label(frame_input, text='NOME DO ALUNO:').grid(row=0, column=0, sticky="w")
entrada_nome = tk.Entry(frame_input, bg=CORES["entrada"], fg=CORES["texto"], insertbackground=CORES["texto"], borderwidth=0)
entrada_nome.grid(row=0, column=1, padx=10, pady=10, ipady=3)

ttk.Label(frame_input, text='NOTA:').grid(row=1, column=0, sticky="w")
entrada_nota = tk.Entry(frame_input, bg=CORES["entrada"], fg=CORES["texto"], insertbackground=CORES["texto"], borderwidth=0, width=10)
entrada_nota.grid(row=1, column=1, padx=10, pady=10, ipady=3, sticky="w")


btn_cadastrar = tk.Button(janela, text="CADASTRAR ALUNO", command=cadastro_aluno, 
                          bg=CORES["btn_confirmar"], fg=CORES["texto"], font=('Helvetica', 9, 'bold'), relief="flat", pady=5)
btn_cadastrar.pack(padx=20, pady=5, fill="x")

btn_nota = tk.Button(janela, text="ADICIONAR NOTA", command=cadastro_nota, 
                     bg=CORES["btn_acao"], fg=CORES["texto"], font=('Helvetica', 9, 'bold'), relief="flat", pady=5)
btn_nota.pack(padx=20, pady=5, fill="x")

btn_media = tk.Button(janela, text="MOSTRAR MÉDIAS", command=calcular_media, 
                      bg=CORES["btn_acao2"], fg=CORES["texto"], font=('Helvetica', 9, 'bold'), relief="flat", pady=5)
btn_media.pack(padx=20, pady=5, fill="x")

btn_excluir = tk.Button(janela, text="EXCLUIR ALUNO", command=excluir_aluno, 
                        bg=CORES["btn_acao3"], fg=CORES["texto"], font=('Helvetica', 9, 'bold'), relief="flat", pady=5)
btn_excluir.pack(padx=20, pady=5, fill="x")


ttk.Label(janela, text='ALUNOS NO SISTEMA:').pack(pady=(15,0))
total_label = ttk.Label(janela, text='')
total_label.pack(pady=(0,5))
lista_alunos = tk.Listbox(janela, bg=CORES["entrada"], fg=CORES["texto"], borderwidth=0, font=('Consolas', 10))
lista_alunos.pack(padx=20, pady=10, fill="both", expand=True)

resultado = tk.Text(janela, height=5, bg=CORES["fundo"], fg=CORES["texto"], borderwidth=0, state="disabled")
resultado.pack(padx=20, pady=10, fill="x")


atualizar_lista()
atualizar_contador()