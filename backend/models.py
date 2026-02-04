from pydantic import BaseModel
from datetime import date
from typing import Optional

class Transaction(BaseModel):
    descricao: str
    valor: float
    categoria: Optional[str] = None
    tipo: str
    data: date 