# 🏫 Sistema de Gestão Acadêmica

Este sistema é a evolução de um projeto de lógica de programação, agora integrado com banco de dados SQL e interface gráfica customizada.

## 🛠️ Tecnologias Utilizadas
- **Python 3.x**
- **SQLite3**: Persistência de dados.
- **Tkinter**: Interface gráfica (UI) em Dark Mode.
- **Hashlib (SHA-256)**: Segurança na autenticação de usuários.

## 📁 Organização do Projeto
Para seguir boas práticas de Engenharia de Software, o sistema foi modularizado:
- `database.py`: Gerenciamento de tabelas e queries SQL.
- `login.py`: Fluxo de autenticação e hashing de segurança.
- `interface.py`: Construção da UI e tratamento de eventos.
- `logica.py`: Regras de negócio e cálculos de médias.

## 🚀 Como testar
1. Clone o repositório.
2. Execute o arquivo `main.py`.
3. Use as credenciais padrão de administrador para o primeiro acesso.

## 🔮 Próximos Passos (Roadmap)
- [ ] **Módulo de Disciplinas:** Adicionar suporte para múltiplas matérias por aluno.
- [ ] **Relatórios:** Gerar médias ponderadas por disciplina.
- [ ] **Níveis de Acesso:** Diferenciar permissões entre Administradores e Professores.
