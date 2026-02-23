from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Dict

#    Pydantic Models

class MaintenanceRecord(BaseModel):
    id: UUID = Field(default_factory= uuid4)
    created_at: datetime = Field(default_factory = datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    equipment_name: str
    description: str
    priority: str
    status: str
    technician: str
    department: str

class MaintenanceRecordCreate(BaseModel):
    equipment_name: str
    description: str
    priority: str
    status: str
    technician: str
    department: str


class MaintenanceRecordUpdate(BaseModel):
    equipment_name: str | None = None
    description: str | None =None
    priority: str | None = None
    status: str | None = None
    technician: str | None = None
    department: str | None = None

#  The Data base

maintenance_db: Dict[UUID, MaintenanceRecord] = {}

app = FastAPI()

#                          Post endpoint

@app.post("/records", status_code=status.HTTP_201_CREATED)
def create_record( record_in: MaintenanceRecordCreate):
    new_record = MaintenanceRecord(**record_in.model_dump())
    maintenance_db[new_record.id] = new_record
    return new_record


#                            GET Endpoints

# Get a record by its ID 

@app.get("/records/{record_id}")
def get_record(record_id: UUID):
    exist = record_id in maintenance_db
    if exist:
        record_exist = maintenance_db[record_id]
        return record_exist
    else:
        raise HTTPException(detail=f"record with id: {str(record_id)} not found", status_code=404)
    
# Get all records

@app.get("/records")
def all_record():
    return list(maintenance_db.values())

# PUT Endpoint

@app.put("/records/{record_id}")
def update_record(record_id:UUID, record_put:MaintenanceRecordCreate):
    exist = record_id in maintenance_db
    updated_record = MaintenanceRecord(**record_put.model_dump())
    if exist:
        existing_record = maintenance_db[record_id]
        updated_record.created_at = existing_record.created_at
        updated_record.id = record_id
        maintenance_db[record_id] = updated_record
        return updated_record
    
    else:
        
        updated_record.id = record_id
        maintenance_db[record_id] = updated_record
        return JSONResponse(content= updated_record.model_dump(mode="json"), status_code=status.HTTP_201_CREATED)
       
    
@app.patch("/records/{record_id}")
def partial_update(record_id: UUID, record_patch: MaintenanceRecordUpdate):
    if record_id not in maintenance_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record {record_id} not found.")
    existing_record = maintenance_db[record_id]
    update_data = record_patch.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_record, field, value)
    existing_record.updated_at = datetime.now()
    maintenance_db[record_id] = existing_record
    
    return existing_record


@app.delete("/records/{record_id}")
def record_delete(record_id: UUID):
    # 1. Guard Clause: Handle 404 first
    if record_id not in maintenance_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Record {record_id} not found."
        )
        
    del maintenance_db[record_id]
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)






    

    


