from typing import Optional
from typing import cast

from fastapi import Depends
from fastapi import FastAPI
from joblib import load
from pydantic import BaseModel
from sklearn.pipeline import Pipeline


class PredictionInput(BaseModel):
    text: str


class PredictionOutput(BaseModel):
    category: str


class NewsgroupsModel:
    model: Optional[Pipeline]
    targets: Optional[list[str]]

    def load_model(self) -> None:
        self.model, self.targets = cast(
            tuple[Pipeline, list[str]], load("newsgroups_model.joblib")
        )

    async def predict(self, input: PredictionInput) -> PredictionOutput:
        if not self.model or not self.targets:
            raise RuntimeError("Model is not loaded")
        prediction = self.model.predict([input.text])
        category = self.targets[prediction[0]]
        return PredictionOutput(category=category)


app = FastAPI()
newgroups_model = NewsgroupsModel()


@app.post("/prediction")
async def prediction(
    output: PredictionOutput = Depends(newgroups_model.predict),
) -> PredictionOutput:
    return output


@app.on_event("startup")  # type: ignore
async def startup() -> None:
    newgroups_model.load_model()
