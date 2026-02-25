"""
ARM AI Configuration and Constants
Centralized configuration management for risk parameters, thresholds, and Firebase settings
"""
import os
from dataclasses import dataclass
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

@dataclass
class RiskThresholds:
    """Risk parameter thresholds for autonomous decision making"""
    MAX_POSITION_SIZE_PERCENT: float = 0.10  # Max 10% of portfolio per position
    MAX_DRAWDOWN_PERCENT: float = 0.15  # 15% max drawdown threshold
    VOLATILITY_THRESHOLD: float = 0.03  # 3% daily volatility threshold
    CORRELATION_THRESHOLD: float = 0.85  # High correlation warning
    LIQUIDITY_MIN_USD: float = 100000.0  # Minimum daily volume
    STOP_LOSS_DEFAULT: float = 0.05  # 5% default stop loss
    TAKE_PROFIT_RATIO: float = 2.0  # 2:1 profit to loss ratio

@dataclass
class FirebaseConfig:
    """Firebase configuration for state management"""
    CREDENTIALS_PATH: str = os.getenv('FIREBASE_CREDENTIALS_PATH', './firebase-credentials.json')
    PROJECT_ID: str = os.getenv('FIREBASE_PROJECT_ID', 'arm-ai-system')
    RISK_EVENTS_COLLECTION: str = 'risk_events'
    PORTFOLIO_STATE_COLLECTION: str = 'portfolio_state'
    MODEL_STATE_COLLECTION: str = 'model_state'

@dataclass
class ModelConfig:
    """Machine learning model configuration"""
    TRAINING_INTERVAL_HOURS: int = 24
    PREDICTION_INTERVAL_MINUTES: int = 5
    ENSEMBLE_WEIGHTS: Dict[str, float] = None
    FEATURE_WINDOW: int = 50  # Lookback period for features
    
    def __post_init__(self):
        if self.ENSEMBLE_WEIGHTS is None:
            self.ENSEMBLE_WEIGHTS = {
                'isolation_forest': 0.3,
                'gradient_boosting': 0.4,
                'lstm': 0.3
            }

class Config:
    """Main configuration class"""
    RISK_THRESHOLDS = RiskThresholds()
    FIREBASE = FirebaseConfig()
    MODELS = ModelConfig()
    
    # API Configuration
    CCXT_TIMEOUT: int = 30000  # 30 seconds
    MAX_RETRIES: int = 3
    REQUEST_DELAY: float = 1.0  # Seconds between requests
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = './logs/arm_ai.log'
    
    # Feature Engineering
    TECHNICAL_INDICATORS = [
        'rsi', 'macd', 'bollinger_upper', 'bollinger_lower',
        'atr', 'volume_ratio', 'vwap', 'momentum'
    ]

# Global configuration instance
config = Config()