from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from powerball_ai import generate_unique_combos  # your existing generator

app = FastAPI()

# Allow Flutter app to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/generate")
def generate_combos(num_combos: int = 10):
    combos = generate_unique_combos(num_combos)
    return {"combinations": combos}
