from sqlalchemy import create_engine
from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from models import  Usuario, Empresa, Feedback, Resposta, BlockChain
from schemas import UsuarioCreate, EmpresaCreate, FeedbackCreate, RespostaCreate, BlockChainCreate
from analysis import feedback_analysis

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
    return {"status": "ok", "message": "Servidor placeholder funcionando!"}

@app.post("/usuarios")
def create_usuario_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/{usuario_id}")
def get_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return usuario

@app.get("/usuarios")
def list_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@app.post("/empresas")
def create_empresa_endpoint(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/{empresa_id}")
def get_empresa_endpoint(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa not found")
    return empresa

@app.get("/empresas")
def list_empresas(db: Session = Depends(get_db)):
    return db.query(Empresa).all()

@app.post("/feedbacks")
def create_feedback_endpoint(feedback: FeedbackCreate, db: Session = Depends(get_db)):

    text= f"{feedback.titulo} {feedback.conteudo}"
    score, confidence = feedback_analysis(text)
    
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

@app.get("/feedbacks/{feedback_id}")
def get_feedback_endpoint(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@app.get("/feedbacks")
def list_feedbacks(db: Session = Depends(get_db)):
    return db.query(Feedback).all()

@app.post("/respostas")
def create_resposta_endpoint(resposta: RespostaCreate, db: Session = Depends(get_db)):
    db_resposta = Resposta(**resposta.dict())
    db.add(db_resposta)
    db.commit()
    db.refresh(db_resposta)
    return db_resposta

@app.get("/respostas/{resposta_id}")
def get_resposta_endpoint(resposta_id: int, db: Session = Depends(get_db)):
    resposta = db.query(Resposta).filter(Resposta.id == resposta_id).first()
    if not resposta:
        raise HTTPException(status_code=404, detail="Resposta not found")
    return resposta

@app.get("/respostas")
def list_respostas(db: Session = Depends(get_db)):
    return db.query(Resposta).all()

@app.post("/blockchains")
def create_blockchain_endpoint(bc: BlockChainCreate, db: Session = Depends(get_db)):
    db_bc = BlockChain(**bc.dict())
    db.add(db_bc)
    db.commit()
    db.refresh(db_bc)
    return db_bc

@app.get("/blockchains/{bc_id}")
def get_blockchain_endpoint(bc_id: int, db: Session = Depends(get_db)):
    bc = db.query(BlockChain).filter(BlockChain.id == bc_id).first()
    if not bc:
        raise HTTPException(status_code=404, detail="BlockChain entry not found")
    return bc

@app.get("/blockchains")
def list_blockchains(db: Session = Depends(get_db)):
    return db.query(BlockChain).all()