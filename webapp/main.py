from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('webapp/templates/index.html')

@app.get("/api/results")
async def get_results():
    with open("results/benchmark_results.json", "r") as f:
        results = json.load(f)
    return results
