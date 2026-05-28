from pydantic import BaseModel


def update_attributes(schema: BaseModel, model):
    for key, value in schema.model_dump(exclude_unset=True).items():
        setattr(model, key, value)
