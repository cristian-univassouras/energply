from typing import Optional
from pydantic import BaseModel
from datetime import date

class CreateReading(BaseModel):
    dia: date
    horario_inicio: str
    horario_fim: str
    leitura_inicio: float
    leitura_fim: float

class ReadingDB(CreateReading):
    id: Optional[str] = None
    consumo_khw: float
    value_real: float
    
