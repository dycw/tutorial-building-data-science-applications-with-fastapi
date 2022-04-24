from typing import Optional
from typing import cast

from joblib import load
from pydantic import BaseModel
from sklearn.pipeline import Pipeline


class PredictionInput(BaseModel):
    text: str


class PredictionOutput(BaseModel):
    category: str


class NewgroupsModel:
    model: Optional[Pipeline]
    targets: Optional[list[str]]

    def load_model(self) -> None:
        self.model, self.targets = cast(
            tuple[Pipeline, list[str]], load("newsgroups_model.joblib")
        )
