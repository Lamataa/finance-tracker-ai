from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal, TransactionDB
from models import Transaction
from datetime import date
from categorizer import categorizador
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Tracker API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas da API
@app.get("/api/despesas/")
def listar_despesas(db: Session = Depends(get_db)):
    despesas = db.query(TransactionDB).all()
    return despesas

@app.post("/api/despesas/")
def adiciona_despesas(despesa: Transaction, db: Session = Depends(get_db)):
    if despesa.categoria is None:
        despesa.categoria = categorizador.categorizar(despesa.descricao)

    nova_despesa = TransactionDB(
        descricao=despesa.descricao,
        valor=despesa.valor,
        categoria=despesa.categoria,
        tipo=despesa.tipo,
        data=despesa.data
    )
    db.add(nova_despesa)
    db.commit()
    db.refresh(nova_despesa)
    return nova_despesa

@app.delete("/api/despesas/{despesa_id}")
def deletar_despesa(despesa_id: int, db: Session = Depends(get_db)):
    despesa = db.query(TransactionDB).filter(TransactionDB.id == despesa_id).first()
    
    if despesa is None:
        return {"message": "Despesa não encontrada"}
    
    db.delete(despesa)
    db.commit()
    return {"message": "Despesa deletada com sucesso"}

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    
    @app.get("/")
    async def read_index():
        return FileResponse(os.path.join(frontend_path, "index.html"))