"""
Módulo de utilitários auxiliares
"""

from .helpers import format_recommendations, calculate_study_time
from .config import BASE_DIR, DATA_DIR, MODEL_PARAMS

__all__ = [
    'format_recommendations',
    'calculate_study_time',
    'BASE_DIR',
    'DATA_DIR',
    'MODEL_PARAMS'
]