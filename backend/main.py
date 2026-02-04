from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal, TransactionDB
from models import Transaction
from datetime import date
from categorizer import categorizador
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/despesas/")
def listar_despesas(db: Session = Depends(get_db)):
    despesass = db.query(TransactionDB).all()
    return despesass

@app.post("/despesas/")
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

@app.delete("/despesas/{despesa_id}")
def deletar_despesa(despesa_id: int, db: Session = Depends(get_db)):
    despesa = db.query(TransactionDB).filter(TransactionDB.id == despesa_id).first()
    
    if despesa is None:
        return {"message": "Despesa não encontrada"}
    
    db.delete(despesa)
    db.commit()

    return {"message": "Despesa deletada com sucesso"}