from pathlib import Path

# Configurações de caminhos
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
MODELS_DIR = BASE_DIR / 'models'

# Parâmetros do modelo
MODEL_PARAMS = {
    'max_recommendations': 5,
    'min_similarity': 0.3
}