from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import declarative_base, Session
from databases import Database

DATABASE_URL = "postgresql://postgres:postgres@10.123.1.100:5432/db"

# Définir les modèles de données SQLAlchemy
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# Initialiser la connexion à la base de données
database = Database(DATABASE_URL)
metadata = MetaData()

# Créer une instance de FastAPI
app = FastAPI()

# Dépendance pour obtenir la session de base de données
def get_db():
    db = database
    try:
        yield db
    finally:
        db.disconnect()

# Créer la table dans la base de données
items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("description", String),
)

# Créer la table dans la base de données (si elle n'existe pas encore)
metadata.create_all(bind=database)

# Définir une route pour créer un élément dans la base de données
@app.post("/items/")
async def create_item(item: Item, db: Session = Depends(get_db)):
    query = items.insert().values(name=item.name, description=item.description)
    last_record_id = await db.execute(query)
    return {"id": last_record_id}

# Définir une route pour obtenir tous les éléments de la base de données
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = items.select().offset(skip).limit(limit)
    items = await db.fetch_all(query)
    return items

