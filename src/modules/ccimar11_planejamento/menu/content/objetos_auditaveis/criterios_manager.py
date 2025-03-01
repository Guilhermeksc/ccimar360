"""
Módulo para gerenciamento de critérios dos objetos auditáveis.

Este módulo contém classes e funções para gerenciar critérios de
materialidade, relevância e criticidade.
"""

import os
import json
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFormLayout, QComboBox, QGroupBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QGridLayout, QWidget
)
from PyQt6.QtCore import Qt
from paths import MAT_RELEV_CRIT_PATH

class CriteriosManager:
    """
    Gerenciador de critérios para objetos auditáveis.
    """
    def __init__(self):
        """
        Inicializa o gerenciador de critérios.
        """
        self.criterios = self.load_criterios()
    
    def load_criterios(self):
        """
        Carrega os critérios do arquivo JSON.
        
        Returns:
            dict: Dicionário com os critérios
        """
        try:
            if os.path.exists(MAT_RELEV_CRIT_PATH):
                with open(MAT_RELEV_CRIT_PATH, 'r', encoding='utf-8') as f:
                    criterios = json.load(f)
                    
                    # Verificar se o formato está correto
                    if not isinstance(criterios, dict):
                        criterios = {
                            "materialidade": [],
                            "relevancia": [],
                            "criticidade": []
                        }
                    
                    # Garantir que todas as chaves existam
                    for tipo in ["materialidade", "relevancia", "criticidade"]:
                        if tipo not in criterios:
                            criterios[tipo] = []
                            
                    return criterios
            
            # Se o arquivo não existir, criar estrutura padrão
            return {
                "materialidade": [],
                "relevancia": [],
                "criticidade": []
            }
        except Exception as e:
            print(f"Erro ao carregar critérios: {e}")
            return {
                "materialidade": [],
                "relevancia": [],
                "criticidade": []
            }
    
    def save_criterios(self):
        """
        Salva os critérios no arquivo JSON.
        """
        try:
            # Garantir que o diretório existe
            os.makedirs(os.path.dirname(MAT_RELEV_CRIT_PATH), exist_ok=True)
            
            with open(MAT_RELEV_CRIT_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.criterios, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar critérios: {e}")
    
    def get_criterios(self, tipo):
        """
        Obtém os critérios de um tipo específico.
        
        Args:
            tipo (str): Tipo de critério (materialidade, relevancia, criticidade)
            
        Returns:
            list: Lista de critérios do tipo especificado
        """
        criterios = self.criterios.get(tipo, [])
        
        # Verificar se criterios é uma lista
        if not isinstance(criterios, list):
            criterios = []
            self.criterios[tipo] = criterios
            self.save_criterios()
            return criterios
        
        # Verificar se os critérios estão no formato correto (lista de dicionários)
        if criterios and len(criterios) > 0 and not isinstance(criterios[0], dict):
            # Converter para o formato esperado
            criterios = [{"nome": criterio, "opcoes": []} for criterio in criterios]
            # Atualizar os critérios
            self.criterios[tipo] = criterios
            # Salvar as alterações
            self.save_criterios()
            
        return criterios
    
    def get_criterio(self, tipo, criterio_id):
        """
        Obtém um critério específico.
        
        Args:
            tipo (str): Tipo de critério (materialidade, relevancia, criticidade)
            criterio_id (str): ID do critério
            
        Returns:
            dict: Critério encontrado ou None se não encontrado
        """
        criterios = self.get_criterios(tipo)
        for criterio in criterios:
            if isinstance(criterio, dict) and criterio.get("id") == criterio_id:
                return criterio
        return None
    
    def add_criterio(self, tipo, criterio):
        """
        Adiciona um critério.
        
        Args:
            tipo (str): Tipo de critério (materialidade, relevancia, criticidade)
            criterio (dict): Critério a ser adicionado
            
        Returns:
            bool: True se o critério foi adicionado com sucesso, False caso contrário
        """
        try:
            if tipo not in self.criterios:
                self.criterios[tipo] = []
            
            self.criterios[tipo].append(criterio)
            self.save_criterios()
            return True
        except Exception as e:
            print(f"Erro ao adicionar critério: {e}")
            return False
    
    def update_criterio(self, tipo, criterio_id, criterio):
        """
        Atualiza um critério.
        
        Args:
            tipo (str): Tipo de critério (materialidade, relevancia, criticidade)
            criterio_id (str): ID do critério
            criterio (dict): Critério atualizado
            
        Returns:
            bool: True se o critério foi atualizado com sucesso, False caso contrário
        """
        try:
            criterios = self.get_criterios(tipo)
            for i, c in enumerate(criterios):
                if isinstance(c, dict) and c.get("id") == criterio_id:
                    self.criterios[tipo][i] = criterio
                    self.save_criterios()
                    return True
            return False
        except Exception as e:
            print(f"Erro ao atualizar critério: {e}")
            return False
    
    def delete_criterio(self, tipo, criterio_id):
        """
        Remove um critério.
        
        Args:
            tipo (str): Tipo de critério (materialidade, relevancia, criticidade)
            criterio_id (str): ID do critério
            
        Returns:
            bool: True se o critério foi removido com sucesso, False caso contrário
        """
        try:
            criterios = self.get_criterios(tipo)
            for i, c in enumerate(criterios):
                if isinstance(c, dict) and c.get("id") == criterio_id:
                    del self.criterios[tipo][i]
                    self.save_criterios()
                    return True
            return False
        except Exception as e:
            print(f"Erro ao remover critério: {e}")
            return False

class CriteriosDialog(QDialog):
    """
    Diálogo para edição de critérios.
    """
    def __init__(self, criterios_manager, tipo, parent=None):
        """
        Inicializa o diálogo de critérios.
        
        Args:
            criterios_manager (CriteriosManager): Gerenciador de critérios
            tipo (str): Tipo de critério (materialidade, relevancia, criticidade)
            parent (QWidget, optional): Widget pai. Padrão é None.
        """
        super().__init__(parent)
        self.setWindowTitle(f"Edição de Critérios - {tipo.title()}")
        self.setModal(True)
        self.resize(800, 600)
        
        self.criterios_manager = criterios_manager
        self.tipo = tipo
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Criar uma tabela para mostrar os critérios
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nome", "Descrição", "Ações"])
        
        # Configurar a tabela
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        # Adicionar a tabela ao layout
        layout.addWidget(self.table)
        
        # Botões
        button_layout = QHBoxLayout()
        
        # Botão Adicionar
        btn_adicionar = QPushButton("Adicionar Critério")
        btn_adicionar.clicked.connect(self.add_criterio)
        button_layout.addWidget(btn_adicionar)
        
        # Botão Fechar
        btn_fechar = QPushButton("Fechar")
        btn_fechar.clicked.connect(self.accept)
        button_layout.addWidget(btn_fechar)
        
        layout.addLayout(button_layout)
        
        # Carregar critérios
        self.load_criterios()
    
    def load_criterios(self):
        """
        Carrega os critérios na tabela.
        """
        # Limpar a tabela
        self.table.setRowCount(0)
        
        # Obter critérios
        criterios = self.criterios_manager.get_criterios(self.tipo)
        
        # Adicionar critérios à tabela
        for criterio in criterios:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Nome do critério
            nome = criterio.get("nome", "") if isinstance(criterio, dict) else criterio
            nome_item = QTableWidgetItem(nome)
            self.table.setItem(row, 0, nome_item)
            
            # Descrição do critério
            descricao = criterio.get("descricao", "") if isinstance(criterio, dict) else ""
            descricao_item = QTableWidgetItem(descricao)
            self.table.setItem(row, 1, descricao_item)
            
            # Botões de ação
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            # Botão Editar
            btn_editar = QPushButton("Editar")
            btn_editar.clicked.connect(lambda checked, r=row: self.edit_criterio(r))
            action_layout.addWidget(btn_editar)
            
            # Botão Excluir
            btn_excluir = QPushButton("Excluir")
            btn_excluir.clicked.connect(lambda checked, r=row: self.delete_criterio(r))
            action_layout.addWidget(btn_excluir)
            
            self.table.setCellWidget(row, 2, action_widget)
    
    def add_criterio(self):
        """
        Adiciona um novo critério.
        """
        # Implementar diálogo para adicionar critério
        pass
    
    def edit_criterio(self, row):
        """
        Edita um critério existente.
        
        Args:
            row (int): Índice da linha do critério
        """
        # Implementar diálogo para editar critério
        pass
    
    def delete_criterio(self, row):
        """
        Remove um critério existente.
        
        Args:
            row (int): Índice da linha do critério
        """
        # Confirmar exclusão
        reply = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            "Tem certeza que deseja excluir este critério?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Obter o ID do critério
            criterios = self.criterios_manager.get_criterios(self.tipo)
            
            # Verificar se o índice é válido
            if row < 0 or row >= len(criterios):
                QMessageBox.critical(self, "Erro", "Índice de critério inválido.")
                return
                
            criterio = criterios[row]
            criterio_id = criterio.get("id") if isinstance(criterio, dict) else criterio
            
            # Remover o critério
            if self.criterios_manager.delete_criterio(self.tipo, criterio_id):
                # Atualizar a tabela
                self.load_criterios()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível excluir o critério.") 