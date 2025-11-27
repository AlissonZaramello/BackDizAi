from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, Boolean, CHAR, Float
from sqlalchemy.ext.declarative import declarative_base
from database import Base

from datetime import datetime

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)
    ativo = Column(Boolean, default=True, nullable=False)
    tipo = Column(String(20), nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=True)

class Empresa(Base):
    __tablename__ = 'empresas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(20), unique=True, nullable=False)
    setor = Column(String(150), nullable=True)
    descricao = Column(Text, nullable=True)

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    empresa_id = Column(Integer, ForeignKey('empresas.id'))
    titulo = Column(String(100), nullable=False)
    conteudo = Column(Text, nullable=False)
    status = Column(String(50), default="Aberto") #aberto, fechado, resolvido
    nota_sentimento = Column(Integer)
    conf_sentimento = Column(Float)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

class Resposta(Base):
    __tablename__ = 'respostas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    feedback_id = Column(Integer, ForeignKey('feedbacks.id'))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    resposta = Column(Text, nullable=False)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

class BlockChain(Base):
    __tablename__ = 'blockchain_hashes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    feedback_id = Column(Integer, ForeignKey('feedbacks.id'))
    hash_feedback = Column(CHAR(64), nullable=False)
    assinatura = Column(Text)
    tx_id_blockchain = Column(String(255))
    rede_blockchain = Column(String(50), nullable=False)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)


