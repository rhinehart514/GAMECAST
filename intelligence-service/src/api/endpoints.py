"""
Intelligence Service API Endpoints

FastAPI endpoints that expose the Puckcast model as a REST API.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from model_client.puckcast_client import get_puckcast_client


# Pydantic models for request/response
class GameStateRequest(BaseModel):
    """Request model for game state."""
    home_team_id: Union[int, str] = Field(..., description="Home team ID or code")
    away_team_id: Union[int, str] = Field(..., description="Away team ID or code")
    period: int = Field(1, ge=1, le=4, description="Period number (1-3, or 4+ for OT)")
    time_remaining: float = Field(60.0, ge=0, description="Minutes remaining in game")
    score_home: int = Field(0, ge=0, description="Home team score")
    score_away: int = Field(0, ge=0, description="Away team score")
    
    # Optional advanced features
    home_fatigue: Optional[float] = Field(None, ge=0, le=1, description="Home team fatigue (0-1)")
    away_fatigue: Optional[float] = Field(None, ge=0, le=1, description="Away team fatigue (0-1)")
    home_xg: Optional[float] = Field(None, ge=0, description="Home expected goals so far")
    away_xg: Optional[float] = Field(None, ge=0, description="Away expected goals so far")
    time_since_last_change: Optional[float] = Field(None, description="Minutes since last line change")
    current_line_fatigue: Optional[float] = Field(None, ge=0, le=1, description="Current line fatigue")
    in_defensive_zone: Optional[bool] = Field(None, description="Is team in defensive zone")
    
    # Team stats for pre-game prediction
    home_stats: Optional[Dict[str, float]] = Field(None, description="Home team season stats")
    away_stats: Optional[Dict[str, float]] = Field(None, description="Away team season stats")


class PredictionResponse(BaseModel):
    """Response model for game prediction."""
    home_win_prob: float = Field(..., description="Home team win probability (0-1)")
    away_win_prob: float = Field(..., description="Away team win probability (0-1)")
    expected_goals_home: float = Field(..., description="Expected final goals for home team")
    expected_goals_away: float = Field(..., description="Expected final goals for away team")
    confidence: float = Field(..., description="Model confidence (0-1)")
    model_version: str = Field(..., description="Model version used")


class DecisionRequest(BaseModel):
    """Request model for decision recommendation."""
    decision_type: str = Field(..., description="Type of decision (line_change, pull_goalie, etc.)")
    options: List[str] = Field(default_factory=list, description="Available options")
    game_state: GameStateRequest = Field(..., description="Current game state")


class DecisionResponse(BaseModel):
    """Response model for decision recommendation."""
    recommendation: str = Field(..., description="Recommended decision")
    confidence: float = Field(..., description="Confidence in recommendation (0-1)")
    reasoning: str = Field(..., description="Explanation of recommendation")
    model_version: str = Field(..., description="Model version used")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_version: str
    model_info: Dict[str, Any]
    timestamp: str


# Create FastAPI app
app = FastAPI(
    title="NHL Intelligence Service",
    description="AI service for NHL simulation game powered by Puckcast model",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    """Initialize model on startup."""
    print("[STARTUP] Starting Intelligence Service...")
    try:
        client = get_puckcast_client()
        print(f"[OK] Model loaded: {client.get_version()}")
    except Exception as e:
        print(f"[ERROR] Error loading model: {e}")
        raise


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "service": "NHL Intelligence Service",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        client = get_puckcast_client()
        info = client.get_info()
        
        return HealthResponse(
            status="healthy",
            model_version=client.get_version(),
            model_info=info,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@app.post("/predict-game", response_model=PredictionResponse)
async def predict_game(request: GameStateRequest):
    """
    Predict game outcome given current state.
    
    This endpoint queries the Puckcast model to predict the probability
    of each team winning based on the current game state.
    """
    try:
        client = get_puckcast_client()
        
        # Convert request to dict
        game_state = request.dict()
        
        # Get prediction from model
        result = client.predict_game_outcome(game_state)
        
        return PredictionResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/recommend-decision", response_model=DecisionResponse)
async def recommend_decision(request: DecisionRequest):
    """
    Recommend best decision from available options.
    
    This endpoint uses the Puckcast model to recommend the optimal
    decision (line change, pull goalie, etc.) given the current game state.
    """
    try:
        client = get_puckcast_client()
        
        # Get recommendation from model
        result = client.recommend_decision(
            decision_type=request.decision_type,
            options=request.options,
            game_state=request.game_state.dict()
        )
        
        # Add model version
        result['model_version'] = client.get_version()
        
        return DecisionResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decision error: {str(e)}")


@app.get("/model/version")
async def get_model_version():
    """Get current model version."""
    try:
        client = get_puckcast_client()
        return {
            "version": client.get_version(),
            "info": client.get_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# CORS middleware (for development)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

