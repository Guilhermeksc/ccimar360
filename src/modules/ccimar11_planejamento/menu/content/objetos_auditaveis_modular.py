"""
Módulo principal para objetos auditáveis (versão modularizada).

Este módulo serve como ponto de entrada para a funcionalidade de objetos auditáveis,
utilizando a estrutura modularizada implementada no pacote objetos_auditaveis.
"""

from .objetos_auditaveis import (
    ObjetosAuditaveisModel,
    MultipicadoresDialog,
    DetalhesDialog,
    CriteriosViewDialog,
    load_multiplicadores,
    save_multiplicadores,
    load_objetos_criterios,
    save_objetos_criterios,
    update_objeto_criterios,
    get_objeto_criterios,
    update_objetos_calculados,
    MultiplicadoresDialog,
    CriteriosManager,
    CustomTableView,
    ExcelModelManager,
    load_config
)
from .objetos_auditaveis.ui import create_objetos_auditaveis

def create_objetos_auditaveis_modular(title_text):
    """
    Cria a interface para objetos auditáveis usando a versão modularizada.
    
    Esta função é um wrapper para a função create_objetos_auditaveis do módulo ui,
    mantendo a mesma assinatura para compatibilidade com o código existente.
    
    Args:
        title_text (str): Texto do título
        database_model: Modelo de banco de dados
        
    Returns:
        QFrame: Frame contendo a interface de objetos auditáveis
    """
    return create_objetos_auditaveis(title_text) 