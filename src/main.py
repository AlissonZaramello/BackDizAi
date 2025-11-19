from sqlalchemy import create_engine
from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
#from analysis import feedback_analysis
from typing import List
from models import  Usuario, Empresa, Feedback, Resposta, BlockChain
from schemas import (
    UsuarioCreate, UsuarioRead,
    EmpresaCreate, EmpresaRead,
    FeedbackCreate, FeedbackRead,
    RespostaCreate, RespostaRead,
    BlockChainCreate, BlockChainRead
)

Base.metadata.create_all(engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "ok", "message": "Servidor acessivel!"}

## USARIOS
@app.post("/usuarios", response_model=UsuarioRead)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
    db.add( db_usuario)
    db.commit()
    db.refresh( db_usuario)
    return  db_usuario

@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    return usuario

@app.get("/usuarios", response_model=List[UsuarioRead])
def list_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@app.put("/usuarios/{usuario_id}", response_model=UsuarioRead)
def update_usuario(usuario_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    for key, value in usuario.dict().items():
        setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).get(usuario_id)
    if not db_usuario:
        raise HTTPException(404,detail= "Usuário não encontrado")
    db.delete(db_usuario)
    db.commit()
    return {"detail": "Usuário deletado com sucesso"}
    
## EMPRESAS
@app.post("/empresas", response_model=EmpresaRead)
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/{empresa_id}", response_model=EmpresaRead)
def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa

@app.get("/empresas", response_model=List[EmpresaRead])
def list_empresas(db: Session = Depends(get_db)):
    return db.query(Empresa).all()

@app.put("/empresas/{empresa_id}", response_model=EmpresaRead)
def update_empresa(empresa_id: int, empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    for key, value in empresa.dict().items():
        setattr(db_empresa, key, value)
    
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.delete("/empresas/{empresa_id}")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).get(empresa_id)
    if not db_empresa:
        raise HTTPException(404, detail="Empresa não encontrada")
    db.delete(db_empresa)
    db.commit()
    return {"detail": "Empresa deletada com sucesso"}

## FEEDBACKS
@app.post("/feedbacks")
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db), response_model=FeedbackRead):

    text= f"{feedback.titulo}, {feedback.conteudo}"
    score, confidence = 0, 0
    #score, confidence = feedback_analysis(text)
    
    db_feedback = Feedback(
        usuario_id=feedback.usuario_id,
        empresa_id=feedback.empresa_id,
        titulo=feedback.titulo,
        conteudo=feedback.conteudo,
        nota_sentimento=score,
        conf_sentimento=confidence
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.get("/feedbacks/{feedback_id}", response_model=FeedbackRead)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail= "Feedback não encontrado")
    return feedback

@app.get("/feedbacks", response_model=List[FeedbackRead])
def list_feedbacks(db: Session = Depends(get_db)):
    return db.query(Feedback).all()

@app.put("/feedbacks/{feedback_id}", response_model=FeedbackRead)
def update_feedback(feedback_id: int, feedback: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = db.query(Feedback).get(feedback_id)
    if not db_feedback:
        raise HTTPException(404, detail= "Feedback não encontrado")
    for key, value in feedback.dict().items():
        setattr(db_feedback, key, value)

    text = f"{db_feedback.titulo}, {db_feedback.conteudo}"
    #db_feedback.nota_sentimento, db_feedback.conf_sentimento = analyze_sentiment(text)
    db_feedback.nota_sentimento, db_feedback.conf_sentimento = 0,0
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.delete("/feedbacks/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(Feedback).get(feedback_id)
    if not db_feedback:
        raise HTTPException(404, detail= "Feedback não encontrado")
    db.delete(db_feedback)
    db.commit()
    return {"detail": "Feedback deletado com sucesso"}

## RESPOSTAS
@app.post("/respostas", response_model=RespostaRead)
def create_resposta(resposta: RespostaCreate, db: Session = Depends(get_db)):
    db_resposta = Resposta(**resposta.dict())
    db.add(db_resposta)
    db.commit()
    db.refresh(db_resposta)
    return db_resposta

@app.get("/respostas/{resposta_id}", response_model=RespostaRead)
def get_resposta(resposta_id: int, db: Session = Depends(get_db)):
    resposta = db.query(Resposta).filter(Resposta.id == resposta_id).first()
    if not resposta:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    return resposta

@app.get("/respostas", response_model=List[RespostaRead])
def list_respostas(db: Session = Depends(get_db)):
    return db.query(Resposta).all()

@app.put("/respostas/{resposta_id}", response_model=RespostaRead)
def update_resposta(resposta_id: int, resposta: RespostaCreate, db: Session = Depends(get_db)):
    db_resposta = db.query(Resposta).get(resposta_id)
    if not db_resposta:
        raise HTTPException(404, detail="Resposta não encontrada")
    for key, value in resposta.dict().items():
        setattr(db_resposta, key, value)
    db.commit()
    db.refresh(db_resposta)
    return db_resposta

@app.delete("/respostas/{resposta_id}")
def delete_resposta(resposta_id: int, db: Session = Depends(get_db)):
    db_resposta = db.query(Resposta).get(resposta_id)
    if not db_resposta:
        raise HTTPException(404, detail="Resposta não encontrada")
    db.delete(db_resposta)
    db.commit()
    return {"detail": "Resposta deletada com sucesso"}

## BLOCKCHAINS
@app.post("/blockchains", response_model=BlockChainRead)
def create_blockchain(bc: BlockChainCreate, db: Session = Depends(get_db)):
    db_bc = BlockChain(**bc.dict())
    db.add(db_bc)
    db.commit()
    db.refresh(db_bc)
    return db_bc

@app.get("/blockchains/{bc_id}", response_model=BlockChainRead)
def get_blockchain(bc_id: int, db: Session = Depends(get_db)):
    bc = db.query(BlockChain).filter(BlockChain.id == bc_id).first()
    if not bc:
        raise HTTPException(status_code=404, detail="BlockChain entry not found")
    return bc

@app.get("/blockchains", response_model=List[BlockChainRead])
def list_blockchains(db: Session = Depends(get_db)):
    return db.query(BlockChain).all()

@app.put("/blockchains/{blockchain_id}", response_model=BlockChainRead)
def update_blockchain(blockchain_id: int, blockchain: BlockChainCreate, db: Session = Depends(get_db)):
    db_block = db.query(BlockChain).get(blockchain_id)
    if not db_block:
        raise HTTPException(404, detail="BlockChain não encontrada")
    for key, value in blockchain.dict().items():
        setattr(db_block, key, value)
    db.commit()
    db.refresh(db_block)
    return db_block

@app.delete("/blockchains/{blockchain_id}")
def delete_blockchain(blockchain_id: int, db: Session = Depends(get_db)):
    db_block = db.query(BlockChain).get(blockchain_id)
    if not db_block:
        raise HTTPException(404,detail= "BlockChain não encontrada")
    db.delete(db_block)
    db.commit()
    return {"detail": "BlockChain deletada com sucesso"}