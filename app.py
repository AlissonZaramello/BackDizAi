from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Servidor placeholder funcionando!"}

@app.get("/create-tables")
def create_tables():
    Base.metadata.create_all(engine)
    return {"status": "Tabelas criadas com sucesso"}
