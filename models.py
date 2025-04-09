from dataclasses import dataclass
from datetime import datetime

@dataclass
class Cedente:
    id: int
    codigo: int
    nome: str
    cgc: str
    tipo: str = "Cedente"
    
    @classmethod
    def from_row(cls, row):
        """Cria um objeto Cedente a partir de uma linha do banco de dados"""
        if row is None:
            return None
        return cls(
            id=row[0],
            codigo=row[1],
            nome=row[2],
            cgc=row[3],
            tipo=row[4]
        )

@dataclass
class Parecer:
    id: int = None
    ctrl_id: int = None
    codigo: int = None
    data: datetime = None
    usuario: str = None
    tipoanotacao: int = 0  # 0 = Negativo, 1 = Positivo
    anotacao: str = ""
    
    @classmethod
    def from_row(cls, row):
        """Cria um objeto Parecer a partir de uma linha do banco de dados"""
        if row is None:
            return None
        return cls(
            id=row[0],
            ctrl_id=row[1],
            codigo=row[2],
            data=row[3],
            usuario=row[4],
            tipoanotacao=row[5],
            anotacao=row[6]
        )
