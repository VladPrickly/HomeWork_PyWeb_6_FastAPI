import uvicorn
from fastapi import FastAPI

app = FastAPI(
    titel="Advertisement",
    description="Buy/Sell Service",
    version="0.0.1",
)


@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}

# if __name__ == '__main__':
#     # uvicorn main:app host=127.0.0.1 port=8000 reload=True
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
