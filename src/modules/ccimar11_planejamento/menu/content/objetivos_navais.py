from PyQt6.QtWidgets import QLabel, QFrame, QHBoxLayout, QVBoxLayout, QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt6.QtCore import Qt

def create_objetivos_navais(title_text, database_model):
    # Frame principal
    content_frame = QFrame()
    content_frame.setStyleSheet("""
        QFrame { 
            padding: 10px;
            background-color: #44475A; 
            border-radius: 8px;
        }
    """)
    main_layout = QHBoxLayout(content_frame)
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)
    
    # Lado esquerdo
    left_frame = QFrame()
    left_layout = QVBoxLayout(left_frame)
    left_layout.setContentsMargins(0, 0, 0, 0)
    left_layout.setSpacing(5)
    
    # Título PEM 2024 com fonte Arial Black
    title_label = QLabel("PEM 2024")
    title_font = QFont("Arial Black", 20)
    title_label.setFont(title_font)
    title_label.setStyleSheet("color: #FFFFFF;")
    left_layout.addWidget(title_label)
    
    # Criação do TreeView
    tree = QTreeView()
    tree.setHeaderHidden(True)
    tree.setStyleSheet("color: #FFF; font-size: 14px;")
    model = QStandardItemModel()
    
    # Definindo as perspectivas e os OBNAV correspondentes
    perspectivas = {
        "Resultados para a Sociedade": list(range(1, 6)),  # OBNAV 1-5
        "Processos": list(range(6, 11)),                   # OBNAV 6-10
        "Institucional": list(range(11, 13))               # OBNAV 11-12
    }
    
    # Popula o modelo com a estrutura: Perspectiva > OBNAV > EN > AEN
    for perspec, obnavs in perspectivas.items():
        perspec_item = QStandardItem(perspec)
        perspec_item.setEditable(False)
        for num in obnavs:
            obnav_item = QStandardItem(f"OBNAV {num}")
            obnav_item.setEditable(False)
            # Adiciona um ou mais filhos EN (exemplo com um filho)
            en_item = QStandardItem("EN - Estratégia Naval")
            en_item.setEditable(False)
            # Adiciona um ou mais filhos AEN ao EN (exemplo com um filho)
            aen_item = QStandardItem("AEN - Ação Estratégica Naval")
            aen_item.setEditable(False)
            en_item.appendRow(aen_item)
            obnav_item.appendRow(en_item)
            perspec_item.appendRow(obnav_item)
        model.appendRow(perspec_item)
    
    tree.setModel(model)
    tree.expandAll()
    left_layout.addWidget(tree)
    
    main_layout.addWidget(left_frame)
    
    # Lado direito (placeholder para conteúdo adicional)
    right_frame = QFrame()
    right_frame.setStyleSheet("background-color: #333; border-radius: 8px;")
    right_frame.setMinimumWidth(200)
    right_layout = QVBoxLayout(right_frame)
    right_layout.setContentsMargins(10, 10, 10, 10)
    placeholder_label = QLabel("Detalhes")
    placeholder_label.setStyleSheet("color: #FFF; font-size: 16px;")
    right_layout.addWidget(placeholder_label)
    
    main_layout.addWidget(right_frame)
    
    return content_frame
