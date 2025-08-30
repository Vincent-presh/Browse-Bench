from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import os
import subprocess
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

class BenchmarkRequest(BaseModel):
    models: list[str]
    test_file: str

@app.get("/")
async def read_index():
    return FileResponse('webapp/templates/index.html')

@app.post("/api/run_benchmark")
async def run_benchmark(request: BenchmarkRequest, background_tasks: BackgroundTasks):
    def run_benchmark_in_background(models, test_file):
        command = [
            "python",
            "-m",
            "services.browsebench.runner",
            "--models",
            *models,
            "--test_file",
            test_file,
        ]
        subprocess.run(command)

    background_tasks.add_task(run_benchmark_in_background, request.models, request.test_file)
    return {"message": "Benchmark run started in the background."}


@app.get("/api/results")
async def get_results():
    if not os.path.exists("results/benchmark_results.json"):
        return JSONResponse(content={})
    with open("results/benchmark_results.json", "r") as f:
        results = json.load(f)
    return results

@app.get("/api/tests")
async def get_tests():
    test_dir = "services/browsebench/tests"
    test_files = [f for f in os.listdir(test_dir) if f.endswith('.yaml')]
    return test_files

@app.get("/api/models")
async def get_models():
    with open("services/browsebench/config/model_configs.json", "r") as f:
        configs = json.load(f)
    return list(configs.keys())
