from pydantic import BaseModel


class TitleRequest(BaseModel):
    title: str
