import os
import pyodbc
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.server = os.getenv("DB_SERVER")
        self.database = os.getenv("DB_DATABASE")
        self.username = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")
        self.app_user = os.getenv("APP_USER", "Sistema")
        
    def connect(self):
        """Estabelece conexão com o banco de dados SQL Server"""
        try:
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
            self.conn = pyodbc.connect(connection_string)
            print("Conexão estabelecida com sucesso!")
            return True
        except pyodbc.Error as e:
            print(f"Erro ao conectar ao banco de dados: {str(e)}")
            return False
    
    def get_user(self):
        """Retorna o nome de usuário definido no arquivo .env"""
        return self.app_user
            
    def search_cedentes(self, term):
        """Busca cedentes pelo termo informado"""
        if not self.conn:
            if not self.connect():
                return []
                
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT TOP(5) id, codigo, nome, cgc, tipo
                FROM sigcad
                WHERE tipo = 'Cedente' AND (
                    nome LIKE ? OR cgc LIKE ? OR codigo LIKE ?
                )
                ORDER BY nome
            """
            search_param = f'%{term}%'
            cursor.execute(query, (search_param, search_param, search_param))
            results = cursor.fetchall()
            cursor.close()
            return results
        except pyodbc.Error as e:
            print(f"Erro ao buscar cedentes: {str(e)}")
            return []
    
    def get_pareceres(self, codigo_cedente):
        """Retorna os pareceres associados ao cedente"""
        if not self.conn:
            if not self.connect():
                return []
                
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT TOP(100) id, ctrl_id, codigo, data, usuario, tipoanotacao, anotacao
                FROM cadanotacao
                WHERE codigo = ?
                ORDER BY data DESC
            """
            cursor.execute(query, (codigo_cedente,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except pyodbc.Error as e:
            print(f"Erro ao buscar pareceres: {str(e)}")
            return []
            
    def get_next_id(self):
        """Obtém o próximo ID disponível para inserção de parecer"""
        if not self.conn:
            if not self.connect():
                return None
                
        try:
            cursor = self.conn.cursor()
            query = "SELECT numero FROM ctrl_id WHERE nome = 'CADANOTACAO'"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return result[0]
            return None
        except pyodbc.Error as e:
            print(f"Erro ao obter próximo ID: {str(e)}")
            return None
    
    def insert_parecer(self, novo_parecer):
        """Insere um novo parecer no banco de dados"""
        if not self.conn:
            if not self.connect():
                return False
        
        try:
            # Obter o próximo ID
            ultimo_id = self.get_next_id()
            if ultimo_id is None:
                return False
            
            novo_id = ultimo_id + 1
            
            # Usar transação nativa do pyodbc
            cursor = self.conn.cursor()
            
            # Inserir novo parecer
            insert_query = """
                INSERT INTO cadanotacao (
                    ctrl_id, codigo, data, usuario, tipoanotacao, anotacao
                ) VALUES (
                    ?, ?, GETDATE(), ?, ?, ?
                )
            """
            cursor.execute(
                insert_query, 
                (novo_id, novo_parecer.codigo, novo_parecer.usuario, 
                novo_parecer.tipoanotacao, novo_parecer.anotacao)
            )
            
            # Atualizar ctrl_id
            update_query = """
                UPDATE ctrl_id 
                SET numero = ?, status = 0
                WHERE nome = 'CADANOTACAO' AND numero = ?
            """
            cursor.execute(update_query, (novo_id, ultimo_id))
            
            # Commit da transação usando o método próprio do pyodbc
            self.conn.commit()
            cursor.close()
            return True
        except pyodbc.Error as e:
            print(f"Erro ao inserir parecer: {str(e)}")
            # Rollback em caso de erro usando o método próprio do pyodbc
            self.conn.rollback()
            return False
