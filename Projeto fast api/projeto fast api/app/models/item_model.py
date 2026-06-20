from sqlalchemy import Column, Integer, String, Float
from app.config.database import Base

class ItemModel(Base):
    __tablename__ = "Agendamento"

    id = Column(Integer, primary_key=True, index=True)
    data_consulta = Column(String, index=True, nullable=False)
    descricao = Column(String, nullable=True)