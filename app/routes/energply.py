from fastapi import  APIRouter, HTTPException
from app.models.leituras import CreateReading, ReadingDB
from app.database import collection
from bson import ObjectId

router = APIRouter()
PRECO_KWH = 0.85


def format_reading(doc) -> ReadingDB:
    doc["id"] = str(doc["_id"])
    return ReadingDB(**doc)

@router.post("/save_reading", response_model=ReadingDB)
async def save_reading(reading: CreateReading):
    
    dados = reading.model_dump()
    dados["dia"] = reading.dia.isoformat()
    dados["consumo_khw"] = (reading.leitura_fim - reading.leitura_inicio) / 1000
    dados["value_real"] = dados["consumo_khw"] * PRECO_KWH
    
    result = await collection.insert_one(dados)

    return ReadingDB(**dados)

@router.get("/get_all_readings", response_model=list[ReadingDB])
async def get_all_readings():
    readings_raw = await collection.find().to_list(length=None)
    return [format_reading(r) for r in readings_raw]


@router.get("/get_reading_by_id/{id}", response_model=ReadingDB)
async def get_reading_by_id(id: str):
    reading = await collection.find_one({"_id": ObjectId(id)})
    if reading:
        return format_reading(reading)

@router.put("/update_reading/{id}", response_model=ReadingDB)
async def update_reading(id: str, reading: CreateReading):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    dados_atualizados = reading.model_dump()
    dados_atualizados["dia"] = reading.dia.isoformat()
    dados_atualizados["consumo_khw"] = (reading.leitura_fim - reading.leitura_inicio) / 1000
    dados_atualizados["value_real"] = dados_atualizados["consumo_khw"] * PRECO_KWH

    result = await collection.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": dados_atualizados}
    )

    if result.matched_count == 1:
        dados_atualizados["id"] = id
        return ReadingDB(**dados_atualizados)
    
    raise HTTPException(status_code=404, detail="Registro não encontrado")


@router.delete("/delete_reading/{id}")
async def delete_reading(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 1:
        return {"message": "Leitura removida com sucesso!"}
    
    raise HTTPException(status_code=404, detail="Registro não encontrado")