def format_recommendations(recommendations):
    """Formata recomendações para exibição"""
    if not recommendations:
        return "Nenhuma recomendação disponível"
    
    formatted = []
    for idx, rec in enumerate(recommendations, 1):
        formatted.append(
            f"Recomendação {idx}:\n"
            f"Matéria: {rec.get('Tópico', 'N/A')}\n"
            f"Conteúdo: {rec.get('Conteúdo', 'N/A')}\n"
            f"Duração: {rec.get('Horas_Estimadas', 'N/A')}h\n"
            f"Dificuldade: {rec.get('Dificuldade', 'N/A')}/5\n"
        )
    return '\n'.join(formatted)

def calculate_study_time(recommendations):
    """Calcula o tempo total de estudo das recomendações"""
    return sum(rec.get('Horas_Estimadas', 0) for rec in recommendations)