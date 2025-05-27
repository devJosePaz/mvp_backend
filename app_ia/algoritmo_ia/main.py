from src.interfaces.cli import get_user_preferences, save_recommendations
from src.models.recommender import StudyRecommender
from src.data_processing.clean_data import load_raw_data, clean_and_merge

def main():
    try:
        # 1. Carregar e preparar dados
        print("⏳ Carregando dados do sistema...")
        math, port = load_raw_data()
        data = clean_and_merge(math, port)
        
        # 2. Inicializar sistema de recomendação
        print("⚙️ Inicializando motor de recomendações...")
        recommender = StudyRecommender(data)
        print("✅ Sistema pronto!\n")
        
        # 3. Modo interativo
        while True:
            try:
                prefs = get_user_preferences()
                if not prefs:  # Usuário cancelou
                    break
                
                print("\n🔍 Buscando recomendações...")
                recs = recommender.recommend(prefs)
                
                # Salva automaticamente em JSON
                saved_file = save_recommendations(recs)
                
                continuar = input("\nDeseja fazer outra consulta? (s/n): ").strip().lower()
                if continuar != 's':
                    print("\nObrigado por usar o sistema! 👋")
                    break
                    
            except KeyboardInterrupt:
                print("\nOperação interrompida pelo usuário.")
                break
            except Exception as e:
                print(f"\n⚠️ Erro: {str(e)}")
                print("Por favor, tente novamente.\n")
                
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {str(e)}")
        print("O sistema não pode ser inicializado.")

if __name__ == "__main__":
    main()