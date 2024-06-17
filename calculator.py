from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import os

app = FastAPI()

class CalculatorRequest(BaseModel):
    operation: str
    num1: float
    num2: float


@app.post("/calculate/")
async def calculate_post(request: CalculatorRequest):
    return calculate(request.num1, request.num2, request.operation)

@app.get("/calculate/")
async def calculate_get(
    num1: float = Query(..., description="Enter first number"),
    num2: float = Query(..., description="Enter second number"),
    operation: str = Query(..., description="Enter operation" )
):
    return calculate(num1, num2, operation)

def calculate(num1: float, num2: float, operation: str):
    operation = operation.lower()
    if operation == "add":
        result = num1 + num2
    elif operation == "sub":
        result = num1 - num2
    elif operation == "mul":
        result = num1 * num2
    elif operation == "div":
        if num2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
        result = num1 / num2
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")
    return {"num1": num1, "num2": num2 , "operation": operation, "result": result}

# Main entry point for the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)