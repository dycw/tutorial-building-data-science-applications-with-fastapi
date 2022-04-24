from joblib import load
from loguru import logger
from sklearn.pipeline import Pipeline


# Load the model
loaded_model: tuple[Pipeline, list[str]] = load("newsgroups_model.joblib")
model, targets = loaded_model


# Run a prediction
p = model.predict(["computer cpu memory ram"])
logger.info(targets[p[0]])
