from sqlalchemy import Column, Integer, String, Float
from app.config.database import Base




class ItemModel(Base):
    __tablename__ = "Agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    Consulta = Column(Float, nullable=False)
    Agendar = Column(String, nullable=True)