from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
async def root():
    raise HTTPException(status_code=404, detail="not implemented")  # endpoint not found


@app.get("/hello")
async def hello_user(name: str = ""):
    if name == "":
        raise HTTPException(
            status_code=400,  # 400 status for bad request, incorrect query parameter provided by user
            detail="Please provide a valid 'name' query parameter",
        )
    greeting = str("hello " + name)
    return greeting
