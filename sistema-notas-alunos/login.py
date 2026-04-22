import tkinter as tk
from tkinter import ttk, messagebox
from database import db_verificar_usuario

def abrir_tela_login():
    login_sucesso = False

    def verificar():
        nonlocal login_sucesso
        usuario = entry_user.get().strip()
        senha = entry_pwd.get().strip()
        
        if db_verificar_usuario(usuario, senha):
            login_sucesso = True
            root_login.destroy()  
        else:
            messagebox.showerror("Erro de Segurança", "Usuário ou senha inválidos!")

    root_login = tk.Tk()
    root_login.title("Autenticação")
    root_login.geometry("300x300") 
    root_login.configure(bg="#1e1e1e")

    
    frame = tk.Frame(root_login, bg="#1e1e1e", padx=20, pady=20)
    frame.pack(expand=True, fill="both")


    ttk.Label(frame, text="Acesso ao Sistema", 
              font=("Helvetica", 12, "bold"), 
              background="#1e1e1e", 
              foreground="white").pack(pady=(0, 15))

    ttk.Label(frame, text="Usuário:", 
              background="#1e1e1e", 
              foreground="white").pack(anchor="w")
    
   
    entry_user = tk.Entry(frame, width=30, bg="#333333", fg="white", 
                          insertbackground="white", borderwidth=0)
    entry_user.pack(pady=(0, 10), ipady=3)
    entry_user.focus() 

   
    ttk.Label(frame, text="Senha:", 
              background="#1e1e1e", 
              foreground="white").pack(anchor="w")
    
    entry_pwd = tk.Entry(frame, width=30, show="*", bg="#333333", 
                         fg="white", insertbackground="white", borderwidth=0)
    entry_pwd.pack(pady=(0, 20), ipady=3)

    
    btn_entrar = tk.Button(frame, text="ENTRAR", command=verificar,
                           bg="#34502b", fg="white", font=("Helvetica", 9, "bold"),
                           relief="flat", cursor="hand2", pady=5)
    btn_entrar.pack(fill="x")

    root_login.bind('<Return>', lambda event: verificar())

    root_login.mainloop()
    return login_sucesso