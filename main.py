from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS", "*"],
    allow_headers=["*"],
)

stored_names = ["Florian", "Tom", "Léo"]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/names")
async def names():
    return {"names": stored_names }


class NameItem(BaseModel):
    name: str


@app.post("/name")
async def post_name(name_item: NameItem):
    stored_names .append(name_item.name)
    return
