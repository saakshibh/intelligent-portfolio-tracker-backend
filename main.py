import sys
import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import HTTPException
import logging

# Ensures the script can find final_sync.py in the same directory
sys.path.append(os.path.dirname(__file__))
from final_sync import analyze_and_sync 

app = FastAPI()

# Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    try:
        # 1. Fallback validation if ticker is blank
        if not request.ticker or not request.ticker.strip():
            raise HTTPException(status_code=400, detail="Ticker cannot be empty")
            
        # 2. Extract and format ticker safely
        ticker = request.ticker.strip().split()[-1].upper()
        logging.info(f"Received sync request targeting ticker token: {ticker}")
        
        # 3. Queue the background machine learning pipeline task
        background_tasks.add_task(analyze_and_sync, [ticker])
        
        return {
            "status": "Analysis started", 
            "ticker": ticker,
            "message": "AI training started. Dashboard will update automatically."
        }
        
    except Exception as e:
        logging.error(f"Internal Pipeline Error: {str(e)}")
        # Returning an explicit HTTP error keeps your CORS headers completely intact!
        raise HTTPException(status_code=500, detail=f"Backend execution dropped: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)