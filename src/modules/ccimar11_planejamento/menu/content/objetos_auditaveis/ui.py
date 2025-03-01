import os
import json
import pandas as pd
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QTableView, QHeaderView,
    QPushButton, QFileDialog, QMessageBox, QStyledItemDelegate
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from paths import CONFIG_PAINT_PATH  # CONFIG_PAINT_PATH = JSON_DIR / "config_paint.json"

import os
import json
import pandas as pd
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QTableView, QHeaderView,
    QPushButton, QFileDialog, QMessageBox, QStyledItemDelegate
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from paths import CONFIG_PAINT_PATH  # CONFIG_PAINT_PATH = JSON_DIR / "config_paint.json"


class CenteredDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter


class CustomTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.verticalHeader().setVisible(False)
        self.setItemDelegate(CenteredDelegate(self))


def load_config():
    """
    Carrega a configuração do arquivo CONFIG_PAINT_PATH.
    Se o arquivo não existir, cria um JSON com valores zerados.
    """
    if os.path.exists(CONFIG_PAINT_PATH):
        try:
            with open(CONFIG_PAINT_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Erro ao carregar a configuração: {e}")
            config = None
        return config
    else:
        default_config = {
            "objetos_auditaveis": [],
            "multiplicador": {
                "materialidade": 0,
                "relevancia": 0,
                "criticidade": 0
            },
            "pontuacao_criterios": {
                "materialidade": [],
                "relevancia": [],
                "criticidade": []
            }
        }
        try:
            with open(CONFIG_PAINT_PATH, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Erro ao criar arquivo de configuração: {e}")
        return default_config


class ExcelModelManager:
    """
    Gerencia a importação e validação do Excel.
    Verifica se:
      - As abas obrigatórias ('Compilado', 'Materialidade', 'Relevância' e 'Criticidade') existem;
      - A aba 'Compilado' possui as colunas 'NR' e 'Objetos Auditáveis';
      - As abas 'Materialidade', 'Relevância' e 'Criticidade' possuem as colunas 'Critério', 'Tipo', 'Descrição' e 'Pontuação'.
    Em caso de erro, exibe uma mensagem via QMessageBox.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.required_sheets = ["Compilado", "Materialidade", "Relevância", "Criticidade"]
        self.required_cols_compilado = ["NR", "Objetos Auditáveis"]
        self.required_cols_others = ["Critério", "Tipo", "Descrição", "Pontuação"]

    def validate(self) -> bool:
        try:
            sheets = pd.read_excel(self.file_path, sheet_name=None)
        except Exception as e:
            self._show_message(f"Erro ao ler o arquivo: {e}")
            return False

        missing_sheets = [sheet for sheet in self.required_sheets if sheet not in sheets]
        if missing_sheets:
            self._show_message("Abas ausentes: " + ", ".join(missing_sheets))
            return False

        errors = []
        compilado = sheets["Compilado"]
        missing_cols_comp = [col for col in self.required_cols_compilado if col not in compilado.columns]
        if missing_cols_comp:
            errors.append("Compilado: " + ", ".join(missing_cols_comp))

        for aba in ["Materialidade", "Relevância", "Criticidade"]:
            df = sheets[aba]
            missing_cols = [col for col in self.required_cols_others if col not in df.columns]
            if missing_cols:
                errors.append(f"{aba}: " + ", ".join(missing_cols))

        if errors:
            self._show_message("Colunas ausentes:\n" + "\n".join(errors))
            return False

        return True

    def _show_message(self, message: str):
        QMessageBox.critical(None, "Erro na Importação", message)


def create_objetos_auditaveis(title_text):
    """
    Cria um QFrame contendo:
      - Um CustomTableView que exibe os dados do modelo carregado a partir do CONFIG_PAINT_PATH.
      - Botões para exportar, importar, gerar relatório e editar multiplicadores.
    As colunas exibidas são fixas:
      ["NR", "Objetos Auditáveis", "Materialidade", "Relevância", "Criticidade", "Total", "Risco"]
    A largura das colunas é definida na proporção:
      Coluna 0: 50, Coluna 1: expansível, Colunas 2 a 5: 70, Coluna 6: 100.
    """
    main_frame = QFrame()
    main_layout = QVBoxLayout(main_frame)
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(15)

    # Título e botões
    title_layout = QHBoxLayout()
    title_label = QLabel("Mapa de Critérios e Pesos")
    title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
    title_layout.addWidget(title_label)
    title_layout.addStretch()

    btn_export = QPushButton("Exportar")
    btn_export.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
    title_layout.addWidget(btn_export)

    btn_import = QPushButton("Importar")
    btn_import.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
    title_layout.addWidget(btn_import)

    btn_report = QPushButton("Relatório")
    btn_report.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
    title_layout.addWidget(btn_report)

    btn_multiplicadores = QPushButton("Multiplicadores")
    btn_multiplicadores.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold;")
    title_layout.addWidget(btn_multiplicadores)

    main_layout.addLayout(title_layout)

    # Cria o CustomTableView e seu modelo
    table_view = CustomTableView()
    model = QStandardItemModel()
    table_view.setModel(model)
    headers = ["NR", "Objetos Auditáveis", "Materialidade", "Relevância", "Criticidade", "Total", "Risco"]
    model.setHorizontalHeaderLabels(headers)
    # Configura tamanhos:
    # Coluna 0: 50, Coluna 1: expansível, Colunas 2-5: 70, Coluna 6: 100.
    table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
    table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    for idx in range(2, 6):
        table_view.horizontalHeader().setSectionResizeMode(idx, QHeaderView.ResizeMode.Fixed)
    table_view.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
    table_view.setColumnWidth(0, 50)
    table_view.setColumnWidth(2, 70)
    table_view.setColumnWidth(3, 70)
    table_view.setColumnWidth(4, 70)
    table_view.setColumnWidth(5, 70)
    table_view.setColumnWidth(6, 100)
    table_view.verticalHeader().setDefaultSectionSize(30)
    main_layout.addWidget(table_view)

    def load_model_from_config():
        """
        Carrega os dados do arquivo de configuração para o CustomTableView.
        Para cada objeto auditável, obtém os valores numéricos de "materialidade",
        "relevancia" e "criticidade" (substituindo NaN por 0) e calcula a coluna "Total"
        como a soma desses valores.
        """
        config = load_config()
        model.clear()
        model.setHorizontalHeaderLabels(headers)
        for item in config.get("objetos_auditaveis", []):
            nr = item.get("nr", "")
            descricao = item.get("descricao", "")
            # Converte valores não numéricos (incluindo NaN) para 0.
            mat_val = sum(v if isinstance(v, (int, float)) else 0 for v in item.get("materialidade", {}).values())
            rel_val = sum(v if isinstance(v, (int, float)) else 0 for v in item.get("relevancia", {}).values())
            crit_val = sum(v if isinstance(v, (int, float)) else 0 for v in item.get("criticidade", {}).values())
            total = mat_val + rel_val + crit_val
            risco = item.get("risco", "")
            row = [
                QStandardItem(str(nr)),
                QStandardItem(str(descricao)),
                QStandardItem(str(mat_val)),
                QStandardItem(str(rel_val)),
                QStandardItem(str(crit_val)),
                QStandardItem(str(total)),
                QStandardItem(str(risco))
            ]
            for cell in row:
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            model.appendRow(row)
        # Reaplica os tamanhos fixos
        table_view.setColumnWidth(0, 50)
        table_view.setColumnWidth(2, 70)
        table_view.setColumnWidth(3, 70)
        table_view.setColumnWidth(4, 70)
        table_view.setColumnWidth(5, 70)
        table_view.setColumnWidth(6, 100)
        table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    load_model_from_config()

    def import_from_excel():
        """
        Função para importar um arquivo Excel.
        Após a importação, a configuração é atualizada e o modelo recarregado.
        Valores NaN são substituídos por 0.
        Além disso, monta o item pai "pontuacao_criterios" com base nos dados das abas.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            main_frame,
            "Importar do Excel",
            "",
            "Arquivos Excel (*.xlsx)"
        )
        if file_path:
            excel_manager = ExcelModelManager(file_path)
            if excel_manager.validate():
                # Ler as planilhas necessárias
                df_compilado = pd.read_excel(file_path, sheet_name="Compilado")
                df_materialidade = pd.read_excel(file_path, sheet_name="Materialidade")
                df_relevancia = pd.read_excel(file_path, sheet_name="Relevância")
                df_criticidade = pd.read_excel(file_path, sheet_name="Criticidade")

                # Monta os objetos auditáveis a partir da aba "Compilado"
                objetos_auditaveis = []
                # Cria dicionários com valor 0 para cada critério (substituindo NaN)
                mat_criterios = df_materialidade["Critério"].dropna().unique().tolist()
                rel_criterios = df_relevancia["Critério"].dropna().unique().tolist()
                crit_criterios = df_criticidade["Critério"].dropna().unique().tolist()
                materialidade_dict = {crit: 0 for crit in mat_criterios}
                relevancia_dict = {crit: 0 for crit in rel_criterios}
                criticidade_dict = {crit: 0 for crit in crit_criterios}
                for _, row in df_compilado.iterrows():
                    nr = row["NR"]
                    descricao = row["Objetos Auditáveis"]
                    objetos_auditaveis.append({
                        "nr": nr,
                        "descricao": descricao,
                        "materialidade": materialidade_dict.copy(),
                        "relevancia": relevancia_dict.copy(),
                        "criticidade": criticidade_dict.copy()
                    })

                # Função auxiliar para construir a pontuação dos critérios a partir de um DataFrame
                def build_pontuacao(df):
                    agrupado = df.groupby("Critério")
                    itens = []
                    for criterio, grupo in agrupado:
                        tipo = grupo["Tipo"].iloc[0]
                        opcoes = []
                        for _, r in grupo.iterrows():
                            opcoes.append({
                                "Descrição": r["Descrição"],
                                "Pontuação": r["Pontuação"]
                            })
                        itens.append({
                            "Critério": criterio,
                            "Tipo": tipo,
                            "opcoes": opcoes
                        })
                    return itens

                pontuacao_criterios = {
                    "relevancia": build_pontuacao(df_relevancia),
                    "materialidade": build_pontuacao(df_materialidade),
                    "criticidade": build_pontuacao(df_criticidade)
                }

                # Monta a configuração completa
                config = {
                    "objetos_auditaveis": objetos_auditaveis,
                    "multiplicador": {
                        "materialidade": 4,
                        "relevancia": 2,
                        "criticidade": 4
                    },
                    "pontuacao_criterios": pontuacao_criterios
                }

                try:
                    with open(CONFIG_PAINT_PATH, "w", encoding="utf-8") as f:
                        json.dump(config, f, indent=4, ensure_ascii=False)
                    QMessageBox.information(main_frame, "Sucesso", "Configuração salva com sucesso!")
                    load_model_from_config()
                    load_model_from_config()  # Recarrega o modelo atualizado
                except Exception as e:
                    QMessageBox.critical(main_frame, "Erro", f"Falha ao salvar a configuração: {e}")

    btn_import.clicked.connect(import_from_excel)
    btn_export.clicked.connect(lambda: print("Exportar"))
    btn_report.clicked.connect(lambda: print("Relatório"))
    btn_multiplicadores.clicked.connect(lambda: print("Multiplicadores"))

    return main_frame
