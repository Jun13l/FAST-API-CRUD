from pydantic import BaseModel
from typing import Optional

# Campos comuns para criação e leitura
class ItemBase(BaseModel):
    nome: str
    preco: float
    descricao: Optional[str] = None

# Schema usado para receber novos itens (entrada)
class ItemCreate(ItemBase):
    pass

# Schema usado para responder requisições (saída com o ID do banco)
class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True