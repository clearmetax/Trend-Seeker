from fastapi import FastAPI, Request
from pydantic import BaseModel
from ai.sentiment import SentimentAnalyzer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SentimentAnalyzer()

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str

@app.post("/classify", response_model=SentimentResponse)
async def classify_sentiment(req: SentimentRequest):
    sentiment = analyzer.classify(req.text)
    return {"sentiment": sentiment} 