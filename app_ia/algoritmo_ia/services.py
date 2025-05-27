from datetime import datetime
import json
from app_ia.algoritmo_ia.src.models.recommender import StudyRecommender
from app_ia.algoritmo_ia.src.data_processing.clean_data import load_raw_data, clean_and_merge

class IARecommendationService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        """Carrega os dados uma vez quando o serviço é criado"""
        print("⏳ Carregando dados do sistema...")
        math, port = load_raw_data()
        self.data = clean_and_merge(math, port)
        print("⚙️ Inicializando motor de recomendações...")
        self.recommender = StudyRecommender(self.data)
        print("✅ Sistema de IA pronto!")

    def gerar_recomendacoes(self, prefs):
        """Gera recomendações no formato do sistema original"""
        try:
            # Adapta para o formato que seu recommender espera
            prefs_adaptadas = {
                "materia": prefs["materia"],
                "nivel": prefs["nivel"],
                "horas": prefs["horas"]
            }
            
            recs = self.recommender.recommend(prefs_adaptadas)
            
            # Formata como no seu CLI original
            output = {
                "recommendations": [],
                "metadata": {
                    "generated_at": datetime.utcnow().isoformat() + "Z",
                    "total_recommendations": len(recs),
                    "total_weekly_hours": sum(r['Horas_Estimadas'] for r in recs)
                }
            }

            for rec in recs:
                recommendation = {
                    "title": rec.get('Tópico', 'Sem título'),
                    "priority": "Alta" if rec.get('Dificuldade', 0) >= 4 else "Média",
                    "category": rec.get('Subtópico', 'Geral'),
                    "description": rec.get('Conteúdo', 'Descrição não disponível'),
                    "weekly_hours": rec['Horas_Estimadas'],
                    "completed": False,
                }
                output["recommendations"].append(recommendation)
            
            return output
            
        except Exception as e:
            print(f"Erro na geração de recomendações: {str(e)}")
            return None