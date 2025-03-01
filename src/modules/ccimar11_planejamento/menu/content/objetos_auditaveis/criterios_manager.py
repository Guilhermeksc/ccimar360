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
    QHeaderView, QMessageBox, QGridLayout, QWidget, QInputDialog
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