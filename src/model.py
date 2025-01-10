import pandas as pd
import joblib
from lightgbm import LGBMClassifier
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from loguru import logger

MODEL_PATH = 'model.pkl'

def prepare_target(df: pd.DataFrame) -> pd.DataFrame:
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
    return df.dropna()

class TradingModel:
    def __init__(self, params: dict):
        self.params = params
        self.model = LGBMClassifier(**params)

    def train(self, df: pd.DataFrame):
        logger.info("Training model with TimeSeriesSplit CV...")
        df = prepare_target(df)
        X = df.drop(columns=['target'])
        y = df['target']
        tscv = TimeSeriesSplit(n_splits=5)
        grid = GridSearchCV(self.model, {
            'num_leaves': [self.params['num_leaves']],
            'learning_rate': [self.params['learning_rate']],
            'n_estimators': [self.params['n_estimators']]
        }, cv=tscv, scoring='accuracy')
        grid.fit(X, y)
        logger.info(f"Best params: {grid.best_params_}")
        self.model = grid.best_estimator_
        preds = self.model.predict(X)
        logger.info(f"Train accuracy: {accuracy_score(y, preds):.4f}")
        logger.info("Classification Report:\n" + classification_report(y, preds))
        joblib.dump(self.model, MODEL_PATH)
        logger.info(f"Model saved to {MODEL_PATH}")

    def predict(self, df: pd.DataFrame) -> int:
        logger.info("Loading model for prediction...")
        self.model = joblib.load(MODEL_PATH)
        X_latest = df.iloc[[-1]].drop(columns=['close', 'volume'], errors='ignore')
        pred = self.model.predict(X_latest)[0]
        logger.info(f"Model prediction: {pred}")
        return pred