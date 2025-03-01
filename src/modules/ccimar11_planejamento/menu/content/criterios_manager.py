import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTreeWidget, QTreeWidgetItem, QInputDialog, QMessageBox,
    QSpinBox, QLineEdit, QFormLayout
)
from PyQt6.QtCore import Qt

class CriterioEditDialog(QDialog):
    def __init__(self, criterio=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Critério")
        self.criterio = criterio if criterio else {"nome": "", "opcoes": []}
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Nome do critério
        form_layout = QFormLayout()
        self.nome_edit = QLineEdit(self.criterio["nome"])
        form_layout.addRow("Nome do Critério:", self.nome_edit)
        layout.addLayout(form_layout)
        
        # Lista de opções
        layout.addWidget(QLabel("Opções:"))
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Descrição", "Pontuação"])
        self.tree.setColumnWidth(0, 300)
        layout.addWidget(self.tree)
        
        # Carregar opções existentes
        for opcao in self.criterio["opcoes"]:
            item = QTreeWidgetItem([opcao["descricao"], str(opcao["pontuacao"])])
            self.tree.addTopLevelItem(item)
        
        # Botões para gerenciar opções
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Adicionar Opção")
        btn_edit = QPushButton("Editar Opção")
        btn_remove = QPushButton("Remover Opção")
        
        btn_add.clicked.connect(self.add_opcao)
        btn_edit.clicked.connect(self.edit_opcao)
        btn_remove.clicked.connect(self.remove_opcao)
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_remove)
        layout.addLayout(btn_layout)
        
        # Botões OK/Cancelar
        buttons = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Cancelar")
        
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        
        buttons.addWidget(btn_ok)
        buttons.addWidget(btn_cancel)
        layout.addLayout(buttons)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
            QLabel {
                color: white;
            }
            QLineEdit, QSpinBox {
                background-color: #3b3b3b;
                color: white;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px 20px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTreeWidget {
                background-color: #3b3b3b;
                color: white;
                border: 1px solid #555;
            }
            QTreeWidget::item:selected {
                background-color: #4CAF50;
            }
        """)

    def add_opcao(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Adicionar Opção")
        layout = QFormLayout(dialog)
        
        desc_edit = QLineEdit()
        pont_spin = QSpinBox()
        pont_spin.setRange(0, 10)
        
        layout.addRow("Descrição:", desc_edit)
        layout.addRow("Pontuação:", pont_spin)
        
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(dialog.accept)
        layout.addRow(btn_ok)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            item = QTreeWidgetItem([desc_edit.text(), str(pont_spin.value())])
            self.tree.addTopLevelItem(item)

    def edit_opcao(self):
        item = self.tree.currentItem()
        if not item:
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Opção")
        layout = QFormLayout(dialog)
        
        desc_edit = QLineEdit(item.text(0))
        pont_spin = QSpinBox()
        pont_spin.setRange(0, 10)
        pont_spin.setValue(int(item.text(1)))
        
        layout.addRow("Descrição:", desc_edit)
        layout.addRow("Pontuação:", pont_spin)
        
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(dialog.accept)
        layout.addRow(btn_ok)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            item.setText(0, desc_edit.text())
            item.setText(1, str(pont_spin.value()))

    def remove_opcao(self):
        item = self.tree.currentItem()
        if item:
            self.tree.takeTopLevelItem(self.tree.indexOfTopLevelItem(item))

    def get_criterio(self):
        criterio = {
            "nome": self.nome_edit.text(),
            "opcoes": []
        }
        
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            criterio["opcoes"].append({
                "descricao": item.text(0),
                "pontuacao": int(item.text(1))
            })
        
        return criterio

class CriteriosManager:
    def __init__(self, json_path):
        self.json_path = Path(json_path)
        self.load_criterios()

    def load_criterios(self):
        if self.json_path.exists():
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.criterios = json.load(f)
        else:
            self.create_default_criterios()

    def create_default_criterios(self):
        self.criterios = {
            "materialidade": {
                "nome": "Materialidade",
                "criterios": [
                    {
                        "nome": "Vulto Financeiro",
                        "opcoes": [
                            {"descricao": "Até 10%", "pontuacao": 1},
                            {"descricao": "De 10% a 20%", "pontuacao": 5},
                            {"descricao": "Acima de 20%", "pontuacao": 10}
                        ]
                    }
                ]
            },
            "relevancia": {
                "nome": "Relevância",
                "criterios": [
                    {
                        "nome": "Vinculação a Ação Estratégica Naval (AEN)",
                        "opcoes": [
                            {"descricao": "Vinculado a uma AEN", "pontuacao": 1},
                            {"descricao": "Vinculado a duas AEN", "pontuacao": 3},
                            {"descricao": "Vinculado a três AEN", "pontuacao": 7},
                            {"descricao": "Vinculado a mais de três AEN", "pontuacao": 10}
                        ]
                    },
                    {
                        "nome": "Vinculação ao Portfólio Estratégico",
                        "opcoes": [
                            {"descricao": "Não", "pontuacao": 0},
                            {"descricao": "Sim", "pontuacao": 10}
                        ]
                    },
                    {
                        "nome": "Vinculação à Ação Orçamentária da LOA",
                        "opcoes": [
                            {"descricao": "Não", "pontuacao": 0},
                            {"descricao": "Sim", "pontuacao": 10}
                        ]
                    }
                ]
            },
            "criticidade": {
                "nome": "Criticidade",
                "criterios": [
                    {
                        "nome": "Tempo sem Auditoria",
                        "opcoes": [
                            {"descricao": "Até 2 anos", "pontuacao": 1},
                            {"descricao": "2 a 3 anos", "pontuacao": 4},
                            {"descricao": "3 a 4 anos", "pontuacao": 7},
                            {"descricao": "Acima de 4 anos", "pontuacao": 10}
                        ]
                    },
                    {
                        "nome": "Eventos Apuratórios Internos (TCE/IPM/Sindicância)",
                        "opcoes": [
                            {"descricao": "Sem registros nos últimos 5 anos", "pontuacao": 1},
                            {"descricao": "Com registro de evento entre 2 a 5 anos", "pontuacao": 4},
                            {"descricao": "Com registro de evento nos últimos 2 anos", "pontuacao": 7},
                            {"descricao": "Com registro reincidente até 2 anos", "pontuacao": 10}
                        ]
                    },
                    {
                        "nome": "Repercussão Externa Negativa (Denúncias/Representações)",
                        "opcoes": [
                            {"descricao": "Sem registro", "pontuacao": 1},
                            {"descricao": "Registro em até 1 ano", "pontuacao": 4},
                            {"descricao": "Registro entre 1 a 2 anos", "pontuacao": 7},
                            {"descricao": "Registro acima de 2 anos", "pontuacao": 10}
                        ]
                    }
                ]
            }
        }
        self.save_criterios()

    def save_criterios(self):
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.criterios, f, indent=4, ensure_ascii=False)

    def get_criterios(self, tipo):
        return self.criterios.get(tipo, {"criterios": []})["criterios"]

    def add_criterio(self, tipo, criterio):
        if tipo not in self.criterios:
            self.criterios[tipo] = {"nome": tipo.capitalize(), "criterios": []}
        self.criterios[tipo]["criterios"].append(criterio)
        self.save_criterios()

    def update_criterio(self, tipo, index, criterio):
        self.criterios[tipo]["criterios"][index] = criterio
        self.save_criterios()

    def remove_criterio(self, tipo, index):
        del self.criterios[tipo]["criterios"][index]
        self.save_criterios()

class CriteriosDialog(QDialog):
    def __init__(self, manager, tipo, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.tipo = tipo
        self.setWindowTitle(f"Editar Critérios - {tipo.capitalize()}")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Lista de critérios
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Critério", "Opções"])
        self.tree.setColumnWidth(0, 300)
        layout.addWidget(self.tree)
        
        # Carregar critérios
        self.load_criterios()
        
        # Botões
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Adicionar Critério")
        btn_edit = QPushButton("Editar Critério")
        btn_remove = QPushButton("Remover Critério")
        
        btn_add.clicked.connect(self.add_criterio)
        btn_edit.clicked.connect(self.edit_criterio)
        btn_remove.clicked.connect(self.remove_criterio)
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_remove)
        layout.addLayout(btn_layout)
        
        # Botão fechar
        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px 20px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTreeWidget {
                background-color: #3b3b3b;
                color: white;
                border: 1px solid #555;
            }
            QTreeWidget::item:selected {
                background-color: #4CAF50;
            }
        """)

    def load_criterios(self):
        self.tree.clear()
        for criterio in self.manager.get_criterios(self.tipo):
            item = QTreeWidgetItem([criterio["nome"]])
            opcoes = ", ".join(f"{op['descricao']} ({op['pontuacao']})" for op in criterio["opcoes"])
            item.setText(1, opcoes)
            self.tree.addTopLevelItem(item)

    def add_criterio(self):
        dialog = CriterioEditDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            criterio = dialog.get_criterio()
            self.manager.add_criterio(self.tipo, criterio)
            self.load_criterios()

    def edit_criterio(self):
        item = self.tree.currentItem()
        if not item:
            return
            
        index = self.tree.indexOfTopLevelItem(item)
        criterio = self.manager.get_criterios(self.tipo)[index]
        
        dialog = CriterioEditDialog(criterio, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            criterio = dialog.get_criterio()
            self.manager.update_criterio(self.tipo, index, criterio)
            self.load_criterios()

    def remove_criterio(self):
        item = self.tree.currentItem()
        if not item:
            return
            
        index = self.tree.indexOfTopLevelItem(item)
        if QMessageBox.question(self, "Confirmar", "Deseja realmente remover este critério?") == QMessageBox.StandardButton.Yes:
            self.manager.remove_criterio(self.tipo, index)
            self.load_criterios() 