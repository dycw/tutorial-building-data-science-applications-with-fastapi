from typing import Optional
from typing import cast

from fastapi import Depends
from fastapi import FastAPI
from fastapi import status
from joblib import Memory
from joblib import load
from pydantic import BaseModel
from sklearn.pipeline import Pipeline


class PredictionInput(BaseModel):
    text: str


class PredictionOutput(BaseModel):
    category: str


memory = Memory(location="cache.joblib")


@memory.cache(ignore=["model"])  # type: ignore
def predict(model: Pipeline, text: str) -> int:
    prediction = model.predict([text])
    return prediction[0]


class NewsgroupsModel:
    model: Optional[Pipeline]
    targets: Optional[list[str]]

    def load_model(self) -> None:
        self.model, self.targets = cast(
            tuple[Pipeline, list[str]], load("newsgroups_model.joblib")
        )

    def predict(self, input: PredictionInput) -> PredictionOutput:
        if not self.model or not self.targets:
            raise RuntimeError("Model is not loaded")
        prediction = predict(self.model, input.text)
        category = self.targets[prediction]
        return PredictionOutput(category=category)


app = FastAPI()
newgroups_model = NewsgroupsModel()


@app.post("/prediction")
def prediction(
    output: PredictionOutput = Depends(newgroups_model.predict),
) -> PredictionOutput:
    return output


@app.delete("/cache", status_code=status.HTTP_204_NO_CONTENT)
def delete_cache() -> None:
    memory.clear()


@app.on_event("startup")  # type: ignore
async def startup() -> None:
    newgroups_model.load_model()
