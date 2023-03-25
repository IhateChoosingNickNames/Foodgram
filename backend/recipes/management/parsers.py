from pydantic import BaseModel


class IngredientParsed(BaseModel):
    name: str
    measurement_unit: str


class IngredientList(BaseModel):
    __root__: list[IngredientParsed]
