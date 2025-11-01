from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, TIMESTAMP, Boolean, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql+psycopg://banco_dizai_user:qhQ2gyuq9S1rVnwNcpCH6YgPawmB5nR7@dpg-d42osver433s73drgib0-a/banco_dizai"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)
    ativo = Column(Boolean, default=True, nullable=False)

class Empresa(Base):
    __tablename__ = 'empresas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    cnpj = Column(String(20), unique=True, nullable=False)
    setor = Column(String(150))
    descricao = Column(Text)
    senha = Column(String(255), nullable=False)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)
    ativo = Column(Boolean, default=True, nullable=False)

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    empresa_id = Column(Integer, ForeignKey('empresas.id'))
    titulo = Column(String(100), nullable=False)
    conteudo = Column(Text, nullable=False)
    status = Column(String(50), default="Aberto") #aberto, em andamento, resolvido
    sentimento = Column(String(50)) #positivo, negativo, neutro
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

class Resposta(Base):
    __tablename__ = 'respostas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    feedback_id = Column(Integer, ForeignKey('feedbacks.id'))
    empresa_id = Column(Integer, ForeignKey('empresas.id'))
    resposta = Column(Text, nullable=False)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

class BlockChain(Base):
    __tablename__ = 'blockchain_hashes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    feedback_id = Column(Integer, ForeignKey('feedbacks.id'))
    hash_feedback = Column(CHAR(64), nullable=False) #SHA-256 do conteudo
    assinatura = Column(Text)
    tx_id_blockchain = Column(String(255)) #id da transação
    rede_blockchain = Column(String(50), nullable=False)
    criado_em = Column(TIMESTAMP, default=datetime.utcnow)

# Cria todas as tabelas no banco
Base.metadata.create_all(engine)
