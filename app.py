from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import MovieDatabase
from recommender import MovieRecommender

# Initialize database and recommender
db = MovieDatabase()
recommender = MovieRecommender(db)

# Create FastAPI app
app = FastAPI(
    title="Movie Recommender API",
    description="Get personalized movie recommendations using collaborative filtering",
    version="1.0"
)

# ==================== DATA MODELS ====================

class RatingRequest(BaseModel):
    """User rating a movie"""
    user_id: int
    movie_id: int
    rating: float  # 1-10 scale
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "movie_id": 1,
                "rating": 8.5
            }
        }

class RecommendationRequest(BaseModel):
    """Request recommendations"""
    user_id: int
    num_recommendations: int = 5
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "num_recommendations": 5
            }
        }

class Movie(BaseModel):
    """Movie details"""
    id: int
    title: str
    year: int
    rating: float

class Recommendation(BaseModel):
    """Movie recommendation"""
    id: int
    title: str
    year: int
    imdb_rating: float
    recommendation_score: float
    reason: str

# ==================== ENDPOINTS ====================

@app.get("/")
def root():
    """Welcome endpoint"""
    return {
        "message": "Movie Recommender API",
        "description": "Get personalized movie recommendations",
        "endpoints": {
            "health": "GET /health - Check API status",
            "movies": "GET /movies - Get all available movies",
            "rate": "POST /rate - Rate a movie",
            "recommend": "POST /recommend - Get recommendations",
            "info": "GET /info - API information",
            "docs": "GET /docs - Interactive documentation"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Movie Recommender API",
        "version": "1.0"
    }

@app.get("/movies", response_model=List[Movie])
def get_movies():
    """Get all available movies"""
    movies = db.get_all_movies()
    return movies

@app.post("/rate")
def rate_movie(request: RatingRequest):
    """
    User rates a movie
    
    Example:
    {
        "user_id": 1,
        "movie_id": 1,
        "rating": 8.5
    }
    """
    
    # Validate rating
    if request.rating < 1 or request.rating > 10:
        raise HTTPException(status_code=400, detail="Rating must be 1-10")
    
    # Check movie exists
    movie = db.get_movie(request.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Save rating
    db.rate_movie(request.user_id, request.movie_id, request.rating)
    
    return {
        "message": "Rating saved",
        "user_id": request.user_id,
        "movie": movie["title"],
        "rating": request.rating
    }

@app.post("/recommend", response_model=List[Recommendation])
def get_recommendations(request: RecommendationRequest):
    """
    Get movie recommendations for a user
    
    Uses collaborative filtering:
    1. Find users with similar taste
    2. Look at movies they rated highly
    3. Recommend those movies
    
    Example:
    {
        "user_id": 1,
        "num_recommendations": 5
    }
    """
    
    # Get recommendations
    recommendations = recommender.get_recommendations(
        request.user_id,
        request.num_recommendations
    )
    
    if not recommendations:
        raise HTTPException(
            status_code=404, 
            detail="No recommendations available. Please rate some movies first."
        )
    
    return recommendations

@app.get("/info")
def api_info():
    """Get API information"""
    return {
        "name": "Movie Recommender API",
        "version": "1.0",
        "algorithm": "Collaborative Filtering (Cosine Similarity)",
        "description": "Recommends movies based on user ratings and similarity to other users",
        "features": [
            "Movie database with 15 classic sci-fi films",
            "User rating system",
            "Collaborative filtering recommendations",
            "RESTful API"
        ],
        "tech_stack": [
            "Python 3.11",
            "FastAPI",
            "SQLite",
            "scikit-learn"
        ]
    }

# ==================== ERROR HANDLERS ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

# ==================== LIFESPAN ====================

@app.on_event("startup")
def startup_event():
    print("Movie Recommender API started")
    print(f"Database: movies.db")
    print(f"Available movies: {len(db.get_all_movies())}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
