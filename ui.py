import sys
import traceback
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QListWidget, QPushButton, 
                            QTextEdit, QRadioButton, QGroupBox, QMessageBox, 
                            QSplitter, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QTimer

from models import Cedente, Parecer
from db import DatabaseConnection

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.init_ui()
        self.current_cedente = None
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.search_cedentes)
        
    def init_ui(self):
        # Configuração da janela principal
        self.setWindowTitle("Sistema de Pareceres - WBA")
        self.resize(1000, 700)
        
        # Layout principal
        main_layout = QVBoxLayout()
        
        # Seção de busca
        search_group = QGroupBox("Buscar Cedente")
        search_layout = QVBoxLayout()
        
        # Campo de busca e resultados
        search_input_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite nome, CNPJ ou código do cedente...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.search_cedentes)
        
        search_input_layout.addWidget(self.search_input)
        search_input_layout.addWidget(search_button)
        
        # Lista de resultados
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.on_cedente_selected)
        
        search_layout.addLayout(search_input_layout)
        search_layout.addWidget(self.results_list)
        search_group.setLayout(search_layout)
        
        # Seção de detalhes do cedente
        cedente_details_group = QGroupBox("Detalhes do Cedente")
        cedente_layout = QVBoxLayout()
        
        cedente_info_layout = QHBoxLayout()
        self.lbl_nome = QLabel("Nome: ")
        self.lbl_codigo = QLabel("Código: ")
        self.lbl_cgc = QLabel("CNPJ: ")
        
        cedente_info_layout.addWidget(self.lbl_nome)
        cedente_info_layout.addWidget(self.lbl_codigo)
        cedente_info_layout.addWidget(self.lbl_cgc)
        
        cedente_layout.addLayout(cedente_info_layout)
        cedente_details_group.setLayout(cedente_layout)
        
        # Splitter para pareceres e inserção
        content_splitter = QSplitter(Qt.Vertical)
        
        # Tabela de pareceres existentes
        pareceres_group = QGroupBox("Pareceres Existentes")
        pareceres_layout = QVBoxLayout()
        
        self.pareceres_table = QTableWidget()
        self.pareceres_table.setColumnCount(6)
        self.pareceres_table.setHorizontalHeaderLabels(["ID", "Data", "Usuário", "Tipo", "Parecer", "Código"])
        self.pareceres_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.pareceres_table.setColumnHidden(5, True)  # Oculta coluna de código
        
        pareceres_layout.addWidget(self.pareceres_table)
        pareceres_group.setLayout(pareceres_layout)
        content_splitter.addWidget(pareceres_group)
        
        # Seção de inserção de parecer
        insert_group = QGroupBox("Inserir Novo Parecer")
        insert_layout = QVBoxLayout()
        
        # Tipo de parecer
        tipo_layout = QHBoxLayout()
        self.radio_positivo = QRadioButton("Positivo")
        self.radio_negativo = QRadioButton("Negativo")
        self.radio_negativo.setChecked(True)  # Default: negativo
        
        tipo_layout.addWidget(self.radio_positivo)
        tipo_layout.addWidget(self.radio_negativo)
        
        # Campo de texto para o parecer
        self.parecer_text = QTextEdit()
        self.parecer_text.setPlaceholderText("Digite aqui seu parecer...")
        
        # Botão de inserção
        self.insert_button = QPushButton("Inserir Parecer")
        self.insert_button.clicked.connect(self.insert_parecer)
        self.insert_button.setEnabled(False)  # Desabilitado até selecionar cedente
        
        insert_layout.addLayout(tipo_layout)
        insert_layout.addWidget(self.parecer_text)
        insert_layout.addWidget(self.insert_button)
        
        insert_group.setLayout(insert_layout)
        content_splitter.addWidget(insert_group)
        
        # Adicionando os elementos ao layout principal
        main_layout.addWidget(search_group, 1)
        main_layout.addWidget(cedente_details_group, 0)
        main_layout.addWidget(content_splitter, 4)
        
        self.setLayout(main_layout)
        
        # Tentar conexão inicial
        if not self.db.connect():
            QMessageBox.critical(self, "Erro de Conexão", 
                                "Não foi possível conectar ao banco de dados. "
                                "Verifique as configurações no arquivo .env")
    
    def on_search_text_changed(self):
        # Atrasa a busca até que o usuário pare de digitar
        self.search_timer.start(300)
        
    def search_cedentes(self):
        search_term = self.search_input.text().strip()
        if len(search_term) < 2:
            return
            
        try:
            results = self.db.search_cedentes(search_term)
            self.results_list.clear()
            
            for row in results:
                cedente = Cedente.from_row(row)
                list_item = f"{cedente.nome} (CNPJ: {cedente.cgc}) - Cód: {cedente.codigo}"
                self.results_list.addItem(list_item)
                self.results_list.item(self.results_list.count() - 1).setData(Qt.UserRole, cedente)
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao buscar cedentes: {str(e)}")
            traceback.print_exc()
            
    def on_cedente_selected(self, item):
        self.current_cedente = item.data(Qt.UserRole)
        
        # Atualizar detalhes do cedente
        self.lbl_nome.setText(f"Nome: {self.current_cedente.nome}")
        self.lbl_codigo.setText(f"Código: {self.current_cedente.codigo}")
        self.lbl_cgc.setText(f"CNPJ: {self.current_cedente.cgc}")
        
        # Habilitar botão de inserção
        self.insert_button.setEnabled(True)
        
        # Carregar pareceres
        self.load_pareceres()
        
    def load_pareceres(self):
        if not self.current_cedente:
            return
            
        try:
            pareceres_rows = self.db.get_pareceres(self.current_cedente.codigo)
            
            # Limpar tabela
            self.pareceres_table.setRowCount(0)
            
            # Preencher tabela
            for row in pareceres_rows:
                parecer = Parecer.from_row(row)
                row_position = self.pareceres_table.rowCount()
                self.pareceres_table.insertRow(row_position)
                
                # Formatar tipo de parecer
                tipo_texto = "Positivo" if parecer.tipoanotacao == 1 else "Negativo"
                
                # Data formatada
                data_formatada = parecer.data.strftime("%d/%m/%Y %H:%M")
                
                # Adicionar dados na tabela
                self.pareceres_table.setItem(row_position, 0, QTableWidgetItem(str(parecer.ctrl_id)))
                self.pareceres_table.setItem(row_position, 1, QTableWidgetItem(data_formatada))
                self.pareceres_table.setItem(row_position, 2, QTableWidgetItem(parecer.usuario))
                self.pareceres_table.setItem(row_position, 3, QTableWidgetItem(tipo_texto))
                self.pareceres_table.setItem(row_position, 4, QTableWidgetItem(parecer.anotacao))
                self.pareceres_table.setItem(row_position, 5, QTableWidgetItem(str(parecer.codigo)))
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar pareceres: {str(e)}")
            traceback.print_exc()
            
    def insert_parecer(self):
        if not self.current_cedente:
            QMessageBox.warning(self, "Aviso", "Selecione um cedente primeiro.")
            return
            
        parecer_texto = self.parecer_text.toPlainText().strip()
        if not parecer_texto:
            QMessageBox.warning(self, "Aviso", "O texto do parecer não pode estar vazio.")
            return
            
        try:
            # Criar objeto parecer
            novo_parecer = Parecer()
            novo_parecer.codigo = self.current_cedente.codigo
            novo_parecer.tipoanotacao = 1 if self.radio_positivo.isChecked() else 0
            novo_parecer.anotacao = parecer_texto
            novo_parecer.usuario = self.db.get_user()
            
            # Inserir no banco
            if self.db.insert_parecer(novo_parecer):
                QMessageBox.information(self, "Sucesso", "Parecer inserido com sucesso!")
                # Limpar campo de texto
                self.parecer_text.clear()
                # Recarregar pareceres
                self.load_pareceres()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível inserir o parecer.")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao inserir parecer: {str(e)}")
            traceback.print_exc()
