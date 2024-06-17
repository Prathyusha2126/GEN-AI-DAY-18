from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import os

app = FastAPI()

class CreateDirectoryRequest(BaseModel):
    path: str

class ListFilesRequest(BaseModel):
    path: str



@app.post("/create_directory/")
async def create_directory(request: CreateDirectoryRequest):
    try:
        os.makedirs(request.path, exist_ok=True)
        return {"message": f"Directory '{request.path}' created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/list_files/")
async def list_files(request: ListFilesRequest):
    try:
        if not os.path.isdir(request.path):
            raise HTTPException(status_code=404, detail="Directory not found")
        files = os.listdir(request.path)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Main entry point for the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)