"""
Módulo para cálculos relacionados aos objetos auditáveis.

Este módulo contém funções para calcular pontuações e totais dos objetos auditáveis.
"""

from .persistence import get_objeto_criterios, update_objeto_criterios

def recalculate_all_objects(criterios_manager):
    """
    Recalcula todos os objetos auditáveis com base nos critérios.
    
    Esta função é usada para atualizar as pontuações de todos os objetos
    quando os critérios ou multiplicadores são alterados.
    
    Args:
        criterios_manager: Gerenciador de critérios
    """
    # Esta função seria implementada para recalcular todos os objetos
    # quando os critérios ou multiplicadores são alterados
    pass

def get_pontuacao_from_descricao(criterios_manager, tipo, descricao):
    """
    Obtém a pontuação correspondente a uma descrição de critério.
    
    Args:
        criterios_manager: Gerenciador de critérios
        tipo (str): Tipo de critério (materialidade, relevancia, criticidade)
        descricao (str): Descrição do critério
        
    Returns:
        int: Pontuação correspondente à descrição ou 0 se não encontrada
    """
    if not descricao:
        return 0
        
    criterios = criterios_manager.get_criterios(tipo)
    
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