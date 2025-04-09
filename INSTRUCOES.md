## **Aplicação - Inserção de Pareceres**

### **Objetivo**
Aplicação desktop leve em Python com interface gráfica (PyQt), para **agilizar o processo de busca de Cedentes e inserção de pareceres** no sistema interno WBA, conectando diretamente ao banco de dados SQL Server (RDS AWS).

---

### **Arquitetura da aplicação**

#### 1. **Camadas**
- `db.py` → Conexão e execução de queries no SQL Server.
- `models.py` → Classes Cedente e Parecer com lógica de dados.
- `ui.py` → Interface com Tkinter (busca, exibição, inserção).
- `main.py` → Inicialização da aplicação.

---

### **Funcionalidades**

#### Busca de Cedente
- Campo de busca por **nome, CNPJ (`cgc`) ou código interno**.
- Sugestões em tempo real com `Listbox` conforme usuário digita.
- Consulta:
```sql
SELECT TOP(5) id, codigo, nome, cgc, tipo
FROM sigcad
WHERE tipo = 'Cedente' AND (
    nome LIKE '%<termo>%'
    OR cgc LIKE '%<termo>%'
    OR codigo LIKE '%<termo>%'
)
ORDER BY nome;
```

---

#### Exibição de pareceres
Ao selecionar um Cedente:
```sql
SELECT TOP(10) id, ctrl_id, codigo, data, usuario, tipoanotacao, anotacao
FROM cadanotacao
WHERE codigo = <codigo_do_cedente>
ORDER BY data DESC;
```

---

#### Inserção de novo parecer
1. Buscar último ID:
```sql
SELECT numero FROM ctrl_id WHERE nome = 'CADANOTACAO';
```

2. Inserir novo parecer:
```sql
INSERT INTO cadanotacao (
  ctrl_id, codigo, data, usuario, tipoanotacao, anotacao
) VALUES (
  <novo_id>, <codigo>, GETDATE(), '<usuario>', <tipoanotacao>, '<anotacao>'
);
```

3. Atualizar `ctrl_id`:
```sql
UPDATE ctrl_id SET numero = <novo_id>, status = 0
WHERE nome = 'CADANOTACAO' AND numero = <ultimo_id>;
```

---

### Estrutura de dados

```python
class Cedente:
    id: int # AUTO-INCREMENT
    codigo: int
    nome: str
    cgc: str
    tipo: str  # sempre "Cedente"

class Parecer:
    id: int # AUTO-INCREMENT
    ctrl_id: int
    codigo: int  # FK para Cedente.codigo
    data: datetime
    usuario: str
    tipoanotacao: int  # 0 = Negativo, 1 = Positivo
    anotacao: str
```

---

### Segurança e boas práticas

- Conexão SQL com `pyodbc` usando `.env` + `python-dotenv`.
- Input sanitizado.
- Consulta assíncrona leve para evitar travar UI.
- Campo "Usuário" obtido de variáveis de ambiente ou input inicial.

---

## PROMPT FINAL

```text
Crie uma aplicação desktop simples em Python com PyQt para inserir pareceres em um sistema interno que utiliza SQL Server hospedado na AWS (RDS). A aplicação se conecta diretamente ao banco de dados "wba".

Funcionalidades:

1. Campo de busca por Cedentes (tabela: sigcad), usando nome, cgc (CNPJ) ou código. Apenas registros com tipo = 'Cedente' devem ser retornados. A busca deve ser dinâmica (ao digitar) e mostrar sugestões em uma lista.

2. Ao selecionar um Cedente, mostrar seus dados (nome, cgc, código) e listar os 100 pareceres mais recentes associados ao seu código. Os pareceres estão na tabela `cadanotacao`.

3. O usuário poderá inserir um novo parecer:
   - Tipo: Positivo (1) ou Negativo (0)
   - Parecer (anotacao)
   - Data: GETDATE()
   - Usuário: capturado do ambiente ou de um valor pré-definido
   - O CTRL_ID do parecer é obtido manualmente via `SELECT numero FROM ctrl_id WHERE nome = 'CADANOTACAO'`
   - Após inserir, deve-se atualizar esse valor com `UPDATE ctrl_id SET numero = <novo_id>, status = 0 WHERE nome = 'CADANOTACAO' AND numero = <ultimo_id>`
   - Explicando: novo_id = ultimo_id + 1

Requisitos técnicos:
- Linguagem: Python 3.10+
- Interface: PyQt
- Banco: SQL Server (via pyodbc)
- Variáveis de conexão devem ser lidas de um arquivo `.env` (use python-dotenv)
- Separe o código em módulos: `db.py`, `models.py`, `ui.py`, `main.py`
- Trate exceções e valide entradas
- Dê prioridade à fluidez de uso e simplicidade visual

Estrutura esperada no banco:

Tabela sigcad:
- id INT (AUTO-INCREMENT)
- codigo INT
- nome VARCHAR
- cgc VARCHAR
- tipo VARCHAR (deve ser sempre 'Cedente')

Tabela cadanotacao:
- id INT (AUTO-INCREMENT)
- ctrl_id INT (manual via tabela ctrl_id)
- codigo INT (FK para Cedente)
- data DATETIME
- usuario VARCHAR
- tipoanotacao INT (0 ou 1)
- anotacao TEXT

Tabela ctrl_id:
- nome VARCHAR (sempre 'CADANOTACAO')
- numero INT
- status INT

Monte o projeto com arquivos separados, código funcional e instruções para rodar localmente.
```