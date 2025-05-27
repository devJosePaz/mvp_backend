from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from unidecode import unidecode  # Adicionado para normalização

class StudyRecommender:
    def __init__(self, data):
        self.data = data
        print("\nInicializando vectorizer...")
        
        # Pré-processamento: normaliza conteúdo removendo acentos
        self.data['Conteúdo_clean'] = self.data['Conteúdo'].apply(
            lambda x: unidecode(x.lower()) if pd.notnull(x) else ""
        )
        
        self.vectorizer = TfidfVectorizer(
            min_df=1,
            max_df=0.9,
            stop_words=None,
            ngram_range=(1, 2),
            token_pattern=r'(?u)\b\w+\b'
        )
        
        self.features = self.vectorizer.fit_transform(self.data['Conteúdo_clean'])
        print(f"Vectorizer pronto! Vocabulário: {len(self.vectorizer.vocabulary_)} termos")

    def recommend(self, user_profile):
        """Gera recomendações com filtros mais robustos"""
        try:
            print(f"\n🔍 Perfil recebido: {user_profile}")
            
            # Normaliza inputs do usuário
            nivel_input = unidecode(user_profile['nivel'].lower())
            materia_input = unidecode(user_profile['materia'].lower())
            horas_input = float(user_profile['horas'])
            
            # Debug: mostra dados disponíveis
            print("Níveis disponíveis:", self.data['Nível'].unique())
            print("Tópicos disponíveis:", self.data['Tópico'].unique())
            
            # Filtro otimizado
            nivel_match = self.data['Nível'].apply(
                lambda x: unidecode(str(x).lower()) == nivel_input
            )
            
            materia_match = self.data['Tópico'].apply(
                lambda x: materia_input in unidecode(str(x).lower())
            )
            
            subset = self.data[nivel_match & materia_match].copy()
            
            # Debug detalhado
            print(f"📊 {len(subset)} tópicos encontrados após filtro inicial")
            if not subset.empty:
                print("Amostra dos tópicos filtrados:")
                print(subset[['Tópico', 'Nível', 'Horas_Estimadas']].head())
            
            if subset.empty:
                print("⚠️ Nenhum tópico encontrado! Relaxando critérios...")
                # Tenta apenas com nível se não achar nada
                subset = self.data[nivel_match].copy()
                print(f"📊 {len(subset)} tópicos encontrados com filtro relaxado")
            
            # Ordenação e seleção
            if not subset.empty:
                indices = subset.index
                sim_matrix = cosine_similarity(self.features[indices])
                
                subset['score'] = np.mean(sim_matrix, axis=1)
                subset = subset.sort_values(['score', 'Horas_Estimadas'], 
                                          ascending=[False, True])
                
                recomendacoes = []
                tempo_total = 0
                
                for _, row in subset.iterrows():
                    if tempo_total + row['Horas_Estimadas'] <= horas_input:
                        recomendacoes.append({
                            'Tópico': row['Tópico'],
                            'Subtópico': row.get('Subtópico', ''),
                            'Conteúdo': row['Conteúdo'],
                            'Horas_Estimadas': float(row['Horas_Estimadas']),
                            'Dificuldade': int(row['Dificuldade'])
                        })
                        tempo_total += row['Horas_Estimadas']
                    
                    if len(recomendacoes) >= 5:  # Limite de recomendações
                        break
                
                print(f"✅ {len(recomendacoes)} recomendações geradas (total: {tempo_total}h)")
                return recomendacoes
            
            return []  # Retorna vazio se não encontrar nada
            
        except Exception as e:
            print(f"🔥 Erro crítico: {str(e)}", exc_info=True)
            return []