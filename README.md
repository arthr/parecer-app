# Aplicação de Pareceres - WBA

Aplicação desktop para inserção de pareceres no sistema interno WBA, conectando diretamente ao banco SQL Server. A aplicação permite buscar cedentes, visualizar pareceres existentes e adicionar novos pareceres de forma rápida e eficiente.

## Requisitos

- Python 3.10 ou superior
- SQL Server com driver ODBC instalado
  - [ODBC Driver 17 para SQL Server](https://go.microsoft.com/fwlink/?linkid=2168524)
- Banco "wba" configurado conforme estrutura especificada
- PyQt5 e demais dependências listadas em `requirements.txt`
- Windows 7, 8, 10 ou 11 (para geração de executável)

## Instalação

### 1. Clone o repositório:
```
git clone [url-do-repositório]
cd parecer-app
```

### 2. Usando ambiente virtual (recomendado):
```
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Instalação direta (alternativa):
```
pip install -r requirements.txt
```

### 4. Configuração do banco de dados:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
DB_SERVER=seu_servidor_aws.amazonaws.com
DB_DATABASE=wba
DB_USERNAME=seu_usuario
DB_PASSWORD=sua_senha
APP_USER=usuario_atual
```

Você pode copiar o arquivo `.env.example` e personalizá-lo:
```
copy .env.example .env
```

## Uso

### Execução em modo desenvolvimento:
```
python main.py
```

### Criação de executável:

#### 1. Instale o PyInstaller:
```
# Se estiver usando ambiente virtual (recomendado)
# Certifique-se de que o ambiente virtual esteja ativado
venv\Scripts\activate  # No Windows
source venv/bin/activate  # No Linux/Mac

# Instale o PyInstaller no ambiente virtual
pip install pyinstaller

# Alternativa: instalação global (fora do ambiente virtual)
# pip install pyinstaller --user
```

#### 2. Gere o executável:
```
# Opção básica (pasta com vários arquivos)
pyinstaller --name="Pareceres-WBA" --windowed --icon=favicon.ico main.py

# Arquivo único (mais lento para iniciar)
pyinstaller --name="Pareceres-WBA" --onefile --windowed --icon=favicon.ico main.py

# Para incluir as variáveis de ambiente no executável
pyinstaller --name="Pareceres-WBA" --onefile --windowed --add-data=".env;." --icon=favicon.ico main.py
```

#### 3. O executável será gerado na pasta `dist/`:
- Modo pasta: `dist/Pareceres-WBA/Pareceres-WBA.exe`
- Modo arquivo único: `dist/Pareceres-WBA.exe`

#### 4. Distribuição:
- Ao distribuir o executável, certifique-se de que o computador de destino tenha o driver ODBC instalado
- Para o modo pasta, distribua toda a pasta `Pareceres-WBA`
- Para o modo arquivo único, basta distribuir o arquivo `.exe`
- Se não incluiu o arquivo `.env` no executável, crie-o no mesmo diretório do executável

> **Nota sobre segurança**: Incluir o arquivo `.env` no executável não é recomendado se ele contiver dados sensíveis como credenciais de banco de dados. Para ambientes de produção, considere distribuir o executável e o arquivo `.env` separadamente ou implementar um mecanismo mais seguro para armazenar credenciais.

## Recursos da aplicação

### 1. Busca de cedentes:
- Digite no campo de busca para encontrar cedentes por nome, CNPJ ou código
- A busca é dinâmica e mostra sugestões à medida que você digita
- Selecione um cedente da lista para ver seus detalhes

### 2. Visualização de pareceres:
- Ao selecionar um cedente, os pareceres associados são exibidos em uma tabela
- Os pareceres são ordenados do mais recente para o mais antigo
- A tabela exibe ID, data, usuário, tipo e texto do parecer

### 3. Inserção de pareceres:
- Escolha o tipo de parecer (Positivo ou Negativo)
- Insira o texto do parecer no campo de texto
- Clique em "Inserir Parecer" para salvar no banco de dados
- A tabela de pareceres é atualizada automaticamente

## Estrutura do Projeto

- `main.py`: Inicializa a aplicação
- `ui.py`: Define a interface gráfica com PyQt
- `db.py`: Gerencia conexões com o banco de dados SQL Server
- `models.py`: Define as classes de dados (Cedente, Parecer)
- `.env`: Configurações de conexão (não incluir no controle de versão)
- `.env.example`: Exemplo de configuração (seguro para controle de versão)
- `requirements.txt`: Lista de dependências do projeto

## Solução de problemas

### Erro de conexão com o banco de dados:
- Verifique se o arquivo `.env` está configurado corretamente
- Confirme se o driver ODBC 17 está instalado
- Verifique se o servidor SQL está acessível da sua rede
- Teste a conexão com outra ferramenta (como SQL Server Management Studio)

### Erro ao executar o programa:
- Certifique-se de que todas as dependências estão instaladas
- Verifique se o Python 3.10+ está instalado e configurado no PATH
- Execute a partir do terminal para ver mensagens de erro detalhadas

### Problemas com o executável:
- Certifique-se de que o driver ODBC está instalado no sistema de destino
- Verifique se há um arquivo `.env` válido no diretório do executável
- Execute o programa a partir de um terminal para ver mensagens de erro
