from pydantic import BaseModel
from typing import Optional

# Usuario
class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioRead(BaseModel):
    id: int
    nome: str
    email: str
    tipo: str
    empresa_id: Optional[int]
    ativo: bool

    class Config:
        from_attributes = True

# Empresa
class EmpresaCreate(BaseModel):
    nome: str
    email: str
    cnpj: str
    senha: str
    setor: Optional[str] = None
    descricao: Optional[str] = None

class EmpresaRead(BaseModel):
    id: int
    cnpj: str
    setor: str
    descricao: str
    nome: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True

# Feedback
class FeedbackCreate(BaseModel):
    usuario_id: int
    empresa_id: int
    titulo: str
    conteudo: str
    nota_sentimento: Optional[int] = None
    conf_sentimento: Optional[float] = None

class FeedbackRead(BaseModel):
    id: int
    usuario_id: int
    empresa_id: int
    titulo: str
    conteudo: str
    status: str
    nota_sentimento: Optional[int]
    conf_sentimento: Optional[float]

    class Config:
        from_attributes = True

# Resposta
class RespostaCreate(BaseModel):
    feedback_id: int
    empresa_id: int
    resposta: str

class RespostaRead(BaseModel):
    id: int
    feedback_id: int
    empresa_id: int
    resposta: str

    class Config:
        from_attributes = True

# BlockChain
class BlockChainCreate(BaseModel):
    feedback_id: int
    hash_feedback: str
    rede_blockchain: str
    assinatura: Optional[str] = None
    tx_id_blockchain: Optional[str] = None

class BlockChainRead(BaseModel):
    id: int
    feedback_id: int
    hash_feedback: str
    rede_blockchain: str
    assinatura: Optional[str]
    tx_id_blockchain: Optional[str]

    class Config:
        from_attributes = True
