import sys
import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensures the script can find final_sync.py in the same directory
sys.path.append(os.path.dirname(__file__))
from final_sync import analyze_and_sync 

app = FastAPI()

# Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    ticker: str

@app.get("/")
async def root():
    return {"message": "SentimentAI Backend is Running"}

@app.post("/analyze")
async def start_analysis(request: StockRequest, background_tasks: BackgroundTasks):
    # Clean ticker before passing to background task
    ticker = request.ticker.split()[-1].strip().upper()
    
    # We use background_tasks so the API returns a response immediately
    background_tasks.add_task(analyze_and_sync, [ticker])
    
    return {
        "status": "Analysis started", 
        "ticker": ticker,
        "message": "AI training started. Dashboard will update automatically in 1-2 minutes."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)