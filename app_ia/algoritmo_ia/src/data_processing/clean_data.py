import pandas as pd
from pathlib import Path
import os

def load_raw_data():
    """Carrega e valida os arquivos CSV com tratamento robusto de erros"""
    try:
        # Caminho absoluto para a pasta de dados
        module_dir = Path(__file__).resolve().parent.parent.parent
        data_dir = module_dir / 'data' / 'raw'
        
        math_path = data_dir / 'matematica.csv'
        port_path = data_dir / 'portugues.csv'

        print(f"🔍 Procurando arquivos em: {data_dir}")

        # Configurações avançadas para leitura de CSV
        csv_config = {
            'encoding': 'utf-8',
            'quotechar': '"',
            'quoting': 1,  # QUOTE_MINIMAL
            'on_bad_lines': 'error',
            'dtype': {
                'Nível': 'str',
                'Tópico': 'str',
                'SubTópico': 'str',
                'Conteúdo': 'str',
                'Horas_Estimadas': 'float64',
                'Dificuldade': 'float64'
            }
        }

        # Leitura com validação
        math = pd.read_csv(math_path, **csv_config)
        port = pd.read_csv(port_path, **csv_config)
        
        # Validação básica de estrutura
        required_columns = ['Nível', 'Tópico', 'SubTópico', 'Conteúdo', 'Horas_Estimadas', 'Dificuldade']
        for df, name in [(math, 'Matemática'), (port, 'Português')]:
            if not all(col in df.columns for col in required_columns):
                missing = [col for col in required_columns if col not in df.columns]
                raise ValueError(f"Colunas faltando em {name}: {missing}")
        
        return math, port
        
    except Exception as e:
        print(f"\n❌ ERRO na carga de dados: {str(e)}")
        print(f"📂 Conteúdo da pasta data/raw: {os.listdir(data_dir) if data_dir.exists() else 'Pasta não existe'}")
        print("💡 Dica: Verifique se os arquivos CSV estão formatados corretamente")
        raise

def clean_and_merge(math_df, port_df):
    """Processamento avançado com tratamento de dados"""
    print("\n🛠️ Iniciando limpeza e combinação de dados...")
    
    try:
        # Normalização de texto
        text_columns = ['Nível', 'Tópico', 'SubTópico', 'Conteúdo']
        for df in [math_df, port_df]:
            for col in text_columns:
                df[col] = df[col].str.strip().str.normalize('NFKC')
            
            # Conversão numérica com tratamento de erros
            df['Horas_Estimadas'] = pd.to_numeric(df['Horas_Estimadas'], errors='coerce')
            df['Dificuldade'] = pd.to_numeric(df['Dificuldade'], errors='coerce')
            
            # Filtro de qualidade
            df.dropna(subset=['Conteúdo', 'Horas_Estimadas'], inplace=True)
            df = df[df['Conteúdo'].astype(bool)]
        
        # Combinação e pós-processamento
        combined = pd.concat([math_df, port_df], ignore_index=True)
        
        # Validação final
        if combined.empty:
            raise ValueError("Dados combinados estão vazios após limpeza")
        
        # Análise de qualidade
        print("\n✅ Dados processados com sucesso!")
        print("📊 Estatísticas:")
        print(f"- Total de tópicos: {len(combined):,}")
        print(f"- Distribuição por nível:")
        print(combined['Nível'].value_counts())
        print(f"- Média de horas por tópico: {combined['Horas_Estimadas'].mean():.1f}h")
        
        return combined
    
    except Exception as e:
        print(f"\n❌ ERRO no processamento: {str(e)}")
        print("💡 Dica: Verifique a consistência dos dados nos arquivos CSV")
        raise