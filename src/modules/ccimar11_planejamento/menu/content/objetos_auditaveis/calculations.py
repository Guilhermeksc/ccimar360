"""
Módulo para cálculos relacionados aos objetos auditáveis.

Este módulo contém funções para calcular pontuações e totais dos objetos auditáveis.
"""

from .persistence import get_objeto_criterios, update_objeto_criterios


def recalculate_objeto(obj, criterios, multiplicadores):
    """
    Recalcula o total e o tipo de risco para um objeto com base nos critérios selecionados.
    
    Args:
        obj (dict): Objeto do CONFIG_PAINT_PATH com os critérios selecionados.
        criterios (dict): Dados de MAT_RELEV_CRIT_PATH.
        multiplicadores (dict): Exemplo: {"materialidade": 1, "relevancia": 1, "criticidade": 1}
        
    Returns:
        dict: Objeto atualizado com 'total' e 'tipo_risco'.
    """
    total = 0
    for tipo in ['materialidade', 'relevancia', 'criticidade']:
        pontuacao = 0
        crit_sel = obj.get(tipo)
        if crit_sel and isinstance(crit_sel, dict):
            criterio_nome = crit_sel.get("Critério")
            valor_selecionado = crit_sel.get("Valor")
            for criterio in criterios.get(tipo, []):
                if criterio.get("Critério") == criterio_nome:
                    for opcao in criterio.get("opcoes", []):
                        if opcao.get("Descrição") == valor_selecionado:
                            pontuacao = opcao.get("Pontuação", 0)
                            break
                    break
        total += pontuacao * multiplicadores.get(tipo, 1)
    
    if total >= 80:
        tipo_risco = "Alto"
    elif total >= 50:
        tipo_risco = "Médio"
    else:
        tipo_risco = "Baixo"
    
    obj["total"] = total
    obj["tipo_risco"] = tipo_risco
    return obj


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