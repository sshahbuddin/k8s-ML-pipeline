from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
async def root():
    raise HTTPException(status_code=404, detail="not implemented")  # endpoint not found


@app.get("/hello")
async def hello_user(name: str = ""):
    if name == "":
        raise HTTPException(
            status_code=422,  # 422 status The request was well-formed but was unable to be followed due to semantic errors.
            detail="Please provide a valid 'name' query parameter",
        )
    greeting = str("hello " + name)
    return greeting
