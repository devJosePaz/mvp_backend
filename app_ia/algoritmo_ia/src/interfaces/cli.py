import json
import os
from datetime import datetime
import unicodedata

def normalize_input(text):
    """Normaliza o texto para comparação: remove acentos, espaços e converte para minúsculas"""
    text = unicodedata.normalize('NFKD', text.lower().strip()).encode('ASCII', 'ignore').decode('ASCII')
    return text.replace(" ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

def get_user_preferences():
    """Coleta preferências do usuário via CLI com validação robusta"""
    print("\n=== Sistema de Recomendação de Estudos ===")
    
    while True:
        try:
            # Coletar nível
            nivel = ""
            niveis_validos = {"basico": "Básico", "intermediario": "Intermediário", "avancado": "Avançado"}
            
            while nivel not in niveis_validos.values():
                entrada = input("Seu nível (Básico/Intermediário/Avançado): ").strip()
                entrada_normalizada = normalize_input(entrada)
                
                for key, value in niveis_validos.items():
                    if entrada_normalizada.startswith(key[:3]):
                        nivel = value
                        break
                
                if nivel not in niveis_validos.values():
                    print("Opção inválida! Use: Básico, Intermediário ou Avançado")
            
            # Coletar horas
            horas = 0
            while horas <= 0:
                try:
                    horas = float(input("Horas disponíveis por semana: "))
                    if horas <= 0:
                        print("Digite um número positivo maior que zero.")
                except ValueError:
                    print("Por favor, digite um número válido.")
            
            # Coletar matéria
            materia = ""
            materias_validas = {"matematica": "Matemática", "portugues": "Português"}
            
            while materia not in materias_validas.values():
                entrada = input("Matéria principal (Matemática/Português): ").strip()
                entrada_normalizada = normalize_input(entrada)
                
                for key, value in materias_validas.items():
                    if entrada_normalizada.startswith(key[:3]):
                        materia = value
                        break
                
                if materia not in materias_validas.values():
                    print("Opção inválida! Escolha entre Matemática ou Português.")
            
            return {
                "nivel": nivel,
                "horas": horas,
                "materia": materia
            }
            
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            return None
        except Exception as e:
            print(f"\nErro inesperado: {str(e)}")
            print("Por favor, tente novamente.\n")

def save_recommendations(recommendations):
    """Salva automaticamente as recomendações em formato JSON"""
    output = {
        "recommendations": [],
        "metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "total_recommendations": len(recommendations),
            "total_weekly_hours": sum(r['Horas_Estimadas'] for r in recommendations)
        }
    }

    for rec in recommendations:
        recommendation = {
            "title": rec.get('Tópico', 'Sem título'),
            "priority": "Alta" if rec.get('Dificuldade', 0) >= 4 else "Média",
            "category": rec.get('Subtópico', 'Geral'),
            "description": rec.get('Conteúdo', 'Descrição não disponível'),
            "weekly_hours": rec['Horas_Estimadas'],
            "completed": False,
        }
        output["recommendations"].append(recommendation)

    filename = f"recomendacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Recomendações salvas automaticamente em '{filename}'")
        return filename
    except Exception as e:
        print(f"\n❌ Erro ao salvar: {str(e)}")
        return None