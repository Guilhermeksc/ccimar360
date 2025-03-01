"""
Módulo para modelos de dados dos objetos auditáveis.

Este módulo contém classes de modelos para representar e manipular
dados de objetos auditáveis.
"""

import os
import json
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from .persistence import get_objeto_criterios, update_objeto_criterios, load_multiplicadores
from paths import MAT_RELEV_CRIT_PATH, CONFIG_PAINT_PATH

class ObjetosAuditaveisModel(QStandardItemModel):
    """
    Modelo para representar objetos auditáveis em uma tabela.
    """
    def __init__(self, criterios_manager, data=None, materialidade_peso=4, relevancia_peso=2, criticidade_peso=4):
        """
        Inicializa o modelo de objetos auditáveis.
        
        Args:
            criterios_manager: Gerenciador de critérios
            data (list, optional): Lista de dados iniciais
            materialidade_peso (int, optional): Peso da materialidade. Padrão é 4.
            relevancia_peso (int, optional): Peso da relevância. Padrão é 2.
            criticidade_peso (int, optional): Peso da criticidade. Padrão é 4.
        """
        super().__init__()
        self.criterios_manager = criterios_manager
        self.materialidade_peso = materialidade_peso
        self.relevancia_peso = relevancia_peso
        self.criticidade_peso = criticidade_peso
        
        # Dicionário para mapear índices de linha para descrições de objetos
        self.row_to_desc = {}
        
        self.setHorizontalHeaderLabels([
            "NR", "Objetos Auditáveis", 
            f"Materialidade\n(x{self.materialidade_peso})",
            f"Relevância\n(x{self.relevancia_peso})", 
            f"Criticidade\n(x{self.criticidade_peso})", 
            "Total", "Tipo de Risco"
        ])
        # Definir flags para tornar os itens não editáveis diretamente
        self.item_flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        
        # Carregar dados dos arquivos de configuração
        if data is None:
            self.load_from_config_files()
        else:
            self.load_data(data)
    
    def load_from_config_files(self):
        """
        Carrega dados dos arquivos de configuração CONFIG_PAINT_PATH e MAT_RELEV_CRIT_PATH.
        """
        try:
            # Carregar multiplicadores
            self.materialidade_peso, self.relevancia_peso, self.criticidade_peso = load_multiplicadores()
            
            # Atualizar cabeçalhos com os novos multiplicadores
            self.setHorizontalHeaderLabels([
                "NR", "Objetos Auditáveis", 
                f"Materialidade\n(x{self.materialidade_peso})",
                f"Relevância\n(x{self.relevancia_peso})", 
                f"Criticidade\n(x{self.criticidade_peso})", 
                "Total", "Tipo de Risco"
            ])
            
            # Carregar objetos do arquivo CONFIG_PAINT_PATH
            objetos_data = []
            if os.path.exists(CONFIG_PAINT_PATH):
                with open(CONFIG_PAINT_PATH, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                    # Verificar se há objetos na configuração
                    if 'objetos' in config and isinstance(config['objetos'], list):
                        for obj in config['objetos']:
                            # Verificar se o objeto tem os campos necessários
                            if 'NR' in obj and 'Objetos Auditáveis' in obj:
                                nr = obj['NR']
                                descricao = obj['Objetos Auditáveis']
                                
                                # Obter critérios do objeto
                                criterios = get_objeto_criterios(descricao) or {}
                                valores_calculados = criterios.get('valores_calculados', {})
                                
                                # Obter valores calculados ou usar valores padrão
                                materialidade = valores_calculados.get('materialidade', 0)
                                relevancia = valores_calculados.get('relevancia', 0)
                                criticidade = valores_calculados.get('criticidade', 0)
                                total = valores_calculados.get('total', 0)
                                tipo_risco = valores_calculados.get('tipo_risco', 'Baixo')
                                
                                # Adicionar à lista de dados
                                objetos_data.append([
                                    nr, descricao, materialidade, relevancia, criticidade, total, tipo_risco
                                ])
            
            # Carregar os dados no modelo
            if objetos_data:
                self.load_data(objetos_data)
            else:
                # Se não houver dados, limpar o modelo
                self.clear()
                self.setHorizontalHeaderLabels([
                    "NR", "Objetos Auditáveis", 
                    f"Materialidade\n(x{self.materialidade_peso})",
                    f"Relevância\n(x{self.relevancia_peso})", 
                    f"Criticidade\n(x{self.criticidade_peso})", 
                    "Total", "Tipo de Risco"
                ])
                
        except Exception as e:
            print(f"Erro ao carregar dados dos arquivos de configuração: {e}")
            # Em caso de erro, limpar o modelo
            self.clear()
            self.setHorizontalHeaderLabels([
                "NR", "Objetos Auditáveis", 
                f"Materialidade\n(x{self.materialidade_peso})",
                f"Relevância\n(x{self.relevancia_peso})", 
                f"Criticidade\n(x{self.criticidade_peso})", 
                "Total", "Tipo de Risco"
            ])
    
    def load_data(self, data):
        """
        Carrega dados no modelo.
        
        Args:
            data (list): Lista de dados a serem carregados
        """
        self.clear()
        self.setHorizontalHeaderLabels([
            "NR", "Objetos Auditáveis", 
            f"Materialidade\n(x{self.materialidade_peso})",
            f"Relevância\n(x{self.relevancia_peso})", 
            f"Criticidade\n(x{self.criticidade_peso})", 
            "Total", "Tipo de Risco"
        ])
        
        # Limpar o mapeamento de linhas para descrições
        self.row_to_desc = {}
        
        # Adicionar os dados
        for row_idx, row_data in enumerate(data):
            # Verificar se temos dados suficientes
            if len(row_data) < 7:
                continue
                
            # Extrair os dados da linha
            nr, descricao, materialidade, relevancia, criticidade, total, tipo_risco = row_data[:7]
            
            # Criar itens para cada coluna
            nr_item = QStandardItem(str(nr))
            nr_item.setFlags(self.item_flags)
            
            desc_item = QStandardItem(descricao)
            desc_item.setFlags(self.item_flags)
            
            mat_item = QStandardItem(str(materialidade))
            mat_item.setFlags(self.item_flags)
            
            rel_item = QStandardItem(str(relevancia))
            rel_item.setFlags(self.item_flags)
            
            crit_item = QStandardItem(str(criticidade))
            crit_item.setFlags(self.item_flags)
            
            total_item = QStandardItem(str(total))
            total_item.setFlags(self.item_flags)
            
            risco_item = QStandardItem(tipo_risco)
            risco_item.setFlags(self.item_flags)
            
            # Adicionar a linha ao modelo
            self.appendRow([nr_item, desc_item, mat_item, rel_item, crit_item, total_item, risco_item])
            
            # Mapear o índice da linha para a descrição do objeto
            self.row_to_desc[row_idx] = descricao
            
            # Carregar critérios do objeto (se existirem)
            objeto_id = descricao
            criterios = get_objeto_criterios(objeto_id)
            
            if criterios:
                # Armazenar os valores originais dos critérios como UserRole
                self.setData(self.index(row_idx, 2), materialidade, Qt.ItemDataRole.UserRole)
                self.setData(self.index(row_idx, 3), relevancia, Qt.ItemDataRole.UserRole)
                self.setData(self.index(row_idx, 4), criticidade, Qt.ItemDataRole.UserRole)
            
            # Recalcular a linha para garantir que os valores estejam corretos
            self.recalculate_row(row_idx)
        
        # Salvar os dados no arquivo de configuração
        self.save_to_config_file()
    
    def save_to_config_file(self):
        """
        Salva os dados do modelo no arquivo de configuração CONFIG_PAINT_PATH.
        """
        try:
            # Carregar configuração existente ou criar nova
            config = {}
            if os.path.exists(CONFIG_PAINT_PATH):
                with open(CONFIG_PAINT_PATH, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            # Atualizar ou criar a lista de objetos
            objetos = []
            for row in range(self.rowCount()):
                nr = self.data(self.index(row, 0))
                descricao = self.data(self.index(row, 1))
                materialidade = float(self.data(self.index(row, 2)) or 0)
                relevancia = float(self.data(self.index(row, 3)) or 0)
                criticidade = float(self.data(self.index(row, 4)) or 0)
                total = float(self.data(self.index(row, 5)) or 0)
                tipo_risco = self.data(self.index(row, 6))
                
                objeto = {
                    'NR': nr,
                    'Objetos Auditáveis': descricao,
                    'materialidade': materialidade,
                    'relevancia': relevancia,
                    'criticidade': criticidade,
                    'total': total,
                    'tipo_risco': tipo_risco
                }
                objetos.append(objeto)
            
            # Atualizar a configuração
            config['objetos'] = objetos
            
            # Garantir que os multiplicadores estejam na configuração
            if 'multiplicadores' not in config:
                config['multiplicadores'] = {
                    'materialidade': self.materialidade_peso,
                    'relevancia': self.relevancia_peso,
                    'criticidade': self.criticidade_peso
                }
            
            # Garantir que o diretório existe
            os.makedirs(os.path.dirname(CONFIG_PAINT_PATH), exist_ok=True)
            
            # Salvar a configuração
            with open(CONFIG_PAINT_PATH, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Erro ao salvar dados no arquivo de configuração: {e}")
    
    def get_row_data(self, row):
        """
        Obtém os dados de uma linha específica.
        
        Args:
            row (int): Índice da linha
            
        Returns:
            list: Lista com os dados da linha
        """
        if row < 0 or row >= self.rowCount():
            return None
            
        return [
            self.data(self.index(row, 0)),
            self.data(self.index(row, 1)),
            self.data(self.index(row, 2)),
            self.data(self.index(row, 3)),
            self.data(self.index(row, 4)),
            self.data(self.index(row, 5)),
            self.data(self.index(row, 6))
        ]
    
    def get_objeto_id(self, row):
        """
        Obtém o ID (descrição) do objeto em uma linha específica.
        
        Args:
            row (int): Índice da linha
            
        Returns:
            str: ID do objeto
        """
        return self.data(self.index(row, 1))
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        """
        Define dados no modelo e recalcula valores se necessário.
        
        Args:
            index (QModelIndex): Índice do item
            value: Valor a ser definido
            role (Qt.ItemDataRole, optional): Papel do item. Padrão é EditRole.
            
        Returns:
            bool: True se os dados foram definidos com sucesso, False caso contrário
        """
        if not index.isValid():
            return False
            
        # Se estamos definindo dados para exibição (EditRole)
        if role == Qt.ItemDataRole.EditRole:
            row = index.row()
            col = index.column()
            
            # Se estamos alterando materialidade, relevância ou criticidade
            if col in [2, 3, 4]:
                # Definir o valor
                result = super().setData(index, value, role)
                
                if result:
                    # Recalcular o total e o tipo de risco
                    self.recalculate_row(row)
                    
                    # Salvar os dados no arquivo de configuração
                    self.save_to_config_file()
                    
                return result
                
        # Para outros papéis, usar a implementação padrão
        return super().setData(index, value, role)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """
        Obtém dados do modelo.
        
        Args:
            index (QModelIndex): Índice do item
            role (Qt.ItemDataRole, optional): Papel do item. Padrão é DisplayRole.
            
        Returns:
            Dados do item
        """
        # Usar a implementação padrão para obter os dados
        return super().data(index, role)
    
    def recalculate_row(self, row):
        """
        Recalcula os valores de uma linha específica.
        
        Args:
            row (int): Índice da linha
        """
        # Obter valores originais dos critérios (armazenados como UserRole)
        materialidade = self.data(self.index(row, 2), Qt.ItemDataRole.UserRole) or float(self.data(self.index(row, 2)) or 0)
        relevancia = self.data(self.index(row, 3), Qt.ItemDataRole.UserRole) or float(self.data(self.index(row, 3)) or 0)
        criticidade = self.data(self.index(row, 4), Qt.ItemDataRole.UserRole) or float(self.data(self.index(row, 4)) or 0)
        
        # Aplicar os pesos
        materialidade_ponderada = materialidade * self.materialidade_peso
        relevancia_ponderada = relevancia * self.relevancia_peso
        criticidade_ponderada = criticidade * self.criticidade_peso
        
        # Calcular o total
        total = materialidade_ponderada + relevancia_ponderada + criticidade_ponderada
        
        # Determinar o tipo de risco com base no total
        tipo_risco = "Baixo"
        if total >= 80:
            tipo_risco = "Alto"
        elif total >= 50:
            tipo_risco = "Médio"
            
        # Atualizar os valores na tabela
        super().setData(self.index(row, 2), str(materialidade))
        super().setData(self.index(row, 3), str(relevancia))
        super().setData(self.index(row, 4), str(criticidade))
        super().setData(self.index(row, 5), str(total))
        super().setData(self.index(row, 6), tipo_risco)
        
        # Obter o ID do objeto
        objeto_id = self.get_objeto_id(row)
        
        # Carregar critérios existentes ou criar novos
        criterios = get_objeto_criterios(objeto_id) or {}
        
        # Atualizar os valores calculados
        if 'valores_calculados' not in criterios:
            criterios['valores_calculados'] = {}
            
        criterios['valores_calculados']['materialidade'] = materialidade
        criterios['valores_calculados']['relevancia'] = relevancia
        criterios['valores_calculados']['criticidade'] = criticidade
        criterios['valores_calculados']['total'] = total
        criterios['valores_calculados']['tipo_risco'] = tipo_risco
        
        # Salvar os critérios atualizados
        update_objeto_criterios(objeto_id, criterios)
    
    def get_pontuacao_from_descricao(self, tipo, descricao):
        """
        Obtém a pontuação correspondente a uma descrição de critério.
        
        Args:
            tipo (str): Tipo de critério (materialidade, relevancia, criticidade)
            descricao (str): Descrição do critério
            
        Returns:
            int: Pontuação correspondente à descrição ou 0 se não encontrada
        """
        if not descricao:
            return 0
            
        criterios = self.criterios_manager.get_criterios(tipo)
        
        for criterio in criterios:
            # Verificar se o critério é um dicionário
            if isinstance(criterio, dict) and "opcoes" in criterio:
                for opcao in criterio["opcoes"]:
                    if opcao.get("descricao") == descricao:
                        return opcao.get("pontuacao", 0)
            # Se for uma string, não tem opções para verificar
            elif isinstance(criterio, str):
                continue
        
        return 0
    
    def get_objetos(self):
        """
        Obtém todos os objetos do modelo.
        
        Returns:
            list: Lista de objetos
        """
        objetos = []
        for row in range(self.rowCount()):
            objeto = {
                'NR': self.data(self.index(row, 0)),
                'Objetos Auditáveis': self.data(self.index(row, 1)),
                'materialidade': float(self.data(self.index(row, 2)) or 0),
                'relevancia': float(self.data(self.index(row, 3)) or 0),
                'criticidade': float(self.data(self.index(row, 4)) or 0),
                'total': float(self.data(self.index(row, 5)) or 0),
                'tipo_risco': self.data(self.index(row, 6))
            }
            objetos.append(objeto)
        return objetos
    
    def flags(self, index):
        """
        Retorna as flags para um item específico.
        
        Args:
            index (QModelIndex): Índice do item
            
        Returns:
            Qt.ItemFlags: Flags do item
        """
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
            
        return self.item_flags
    
    def update_multiplicadores(self, materialidade_peso, relevancia_peso, criticidade_peso):
        """
        Atualiza os multiplicadores e recalcula todos os valores.
        
        Args:
            materialidade_peso (int): Novo peso da materialidade
            relevancia_peso (int): Novo peso da relevância
            criticidade_peso (int): Novo peso da criticidade
        """
        # Atualizar os pesos
        self.materialidade_peso = materialidade_peso
        self.relevancia_peso = relevancia_peso
        self.criticidade_peso = criticidade_peso
        
        # Atualizar os cabeçalhos
        self.setHorizontalHeaderLabels([
            "NR", "Objetos Auditáveis", 
            f"Materialidade\n(x{self.materialidade_peso})",
            f"Relevância\n(x{self.relevancia_peso})", 
            f"Criticidade\n(x{self.criticidade_peso})", 
            "Total", "Tipo de Risco"
        ])
        
        # Recalcular todas as linhas
        for row in range(self.rowCount()):
            self.recalculate_row(row)
        
        # Salvar os dados no arquivo de configuração
        self.save_to_config_file()
    
    def clear(self):
        """
        Limpa o modelo e o mapeamento de linhas para descrições.
        """
        super().clear()
        self.row_to_desc = {} 