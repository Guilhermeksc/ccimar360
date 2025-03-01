"""
Pacote objetos_auditaveis.

Este pacote contém os módulos relacionados à gestão de objetos auditáveis,
incluindo modelos, diálogos, persistência, cálculos e interface do usuário.
"""

from .models import ObjetosAuditaveisModel
from .dialogs import MultipicadoresDialog, DetalhesDialog, CriteriosViewDialog
from .persistence import (
    load_multiplicadores, save_multiplicadores,
    load_objetos_criterios, save_objetos_criterios,
    update_objeto_criterios, get_objeto_criterios,
    update_objetos_calculados
)
from .calculations import (
    recalculate_objeto,
    get_pontuacao_from_descricao
)
from .ui import create_objetos_auditaveis
from .criterios_manager import CriteriosManager

__all__ = [
    'ObjetosAuditaveisModel',
    'MultipicadoresDialog',
    'DetalhesDialog',
    'CriteriosViewDialog',
    'load_multiplicadores',
    'save_multiplicadores',
    'load_objetos_criterios',
    'save_objetos_criterios',
    'update_objeto_criterios',
    'get_objeto_criterios',
    'update_objetos_calculados',
    'recalculate_all_objects',
    'get_pontuacao_from_descricao',
    'create_objetos_auditaveis',
    'CriteriosManager',
    'CriteriosDialog'
] 