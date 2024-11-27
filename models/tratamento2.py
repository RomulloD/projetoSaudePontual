from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Tratamento2(BaseModel):
    data_inicio: Optional[datetime] = None
    data_finalizacao: Optional[datetime] = None
    medicamento_id: int
    lembrete_tomar_remedio: Optional[datetime] = None
    lembrete_remedio_acabando: Optional[datetime] = None