from database import criar_tabelas
from login import abrir_tela_login
from interface import janela

if __name__ == "__main__":
    criar_tabelas()
    
    if abrir_tela_login():
        janela.mainloop()