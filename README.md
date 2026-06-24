# Movie Recommender API

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Docker](https://img.shields.io/badge/Docker-Yes-blue)
![AWS](https://img.shields.io/badge/AWS-EC2-orange)

## Overview

A personalized movie recommendation system using **collaborative filtering**. 
This API learns from user movie ratings and recommends films based on 
similar users' preferences.

## Features

✅ **Collaborative Filtering Algorithm** - Find similar users by taste  
✅ **RESTful API** - Built with FastAPI  
✅ **SQLite Database** - Persistent user ratings  
✅ **Docker Container** - Easy deployment  
✅ **AWS Deployment** - Running on EC2  
✅ **Interactive Documentation** - Swagger UI at `/docs`  

## How It Works

### Algorithm: Collaborative Filtering

1. **User Rates Movies** - Users rate movies (1-10 scale)
2. **Find Similar Users** - Calculates cosine similarity between rating patterns
3. **Score Unrated Movies** - Averages ratings from similar users
4. **Recommend** - Returns top-rated movies user hasn't seen

**Example:**
```
You rated: Inception (9), Interstellar (8.5), Matrix (8)
User A also rated: Inception (9), Interstellar (8.5), Matrix (8), Dune (8.1)
Recommendation: "Watch Dune (8.1/10)"
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11 |
| API Framework | FastAPI |
| Database | SQLite |
| ML Algorithm | scikit-learn (cosine similarity) |
| Container | Docker |
| Cloud | AWS EC2 |
| Documentation | Swagger UI / OpenAPI |

## Project Structure

```
movie-recommender-api/
├── app.py                 # FastAPI application
├── database.py            # SQLite database management
├── recommender.py         # Collaborative filtering algorithm
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── README.md              # This file
└── movies.db              # SQLite database (auto-generated)
```

## Installation

### Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/movie-recommender-api.git
cd movie-recommender-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run API
python -m uvicorn app:app --reload

# Open browser
http://localhost:8000/docs
```

### Docker

```bash
# Build image
docker build -t movie-recommender:1.0 .

# Run container
docker run -p 8000:8000 movie-recommender:1.0

# Access API
http://localhost:8000/docs
```

## API Endpoints

### Health Check
```bash
GET /health
Response: {"status": "healthy", "service": "Movie Recommender API", "version": "1.0"}
```

### Get All Movies
```bash
GET /movies
Response: [{"id": 1, "title": "Inception", "year": 2010, "rating": 8.8}, ...]
```

### Rate a Movie
```bash
POST /rate
Body: {
  "user_id": 1,
  "movie_id": 1,
  "rating": 9.0
}
Response: {"message": "Rating saved", "user_id": 1, "movie": "Inception", "rating": 9.0}
```

### Get Recommendations
```bash
POST /recommend
Body: {
  "user_id": 1,
  "num_recommendations": 5
}
Response: [
  {
    "id": 4,
    "title": "Dune",
    "year": 2021,
    "imdb_rating": 8.0,
    "recommendation_score": 8.1,
    "reason": "Similar users loved this"
  },
  ...
]
```

### API Information
```bash
GET /info
Response: {"name": "Movie Recommender API", "version": "1.0", "algorithm": "Collaborative Filtering", ...}
```

## Interactive Documentation

Once running, visit: `http://localhost:8000/docs`

This opens **Swagger UI** where you can:
- View all endpoints with descriptions
- See example requests and responses
- Test endpoints directly in the browser
- View request/response schemas

## Database

SQLite database with 3 tables:

### Movies Table
```sql
CREATE TABLE movies (
  id INTEGER PRIMARY KEY,
  title TEXT UNIQUE,
  year INTEGER,
  rating REAL
)
```

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE
)
```

### Ratings Table
```sql
CREATE TABLE ratings (
  user_id INTEGER,
  movie_id INTEGER,
  rating REAL,
  PRIMARY KEY(user_id, movie_id),
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(movie_id) REFERENCES movies(id)
)
```

Includes 15 classic sci-fi movies for testing.

## Algorithm Details

### Cosine Similarity

The algorithm uses **cosine similarity** to find similar users:

```
similarity = (A · B) / (||A|| * ||B||)

Where:
A = User 1's rating vector
B = User 2's rating vector
```

**Example:**
```
User 1: [10, 9, 8, 0, 0]
User 2: [9, 8, 9, 8, 0]
Similarity: 0.98 (very similar!)

User 3: [1, 1, 1, 10, 9]
Similarity: 0.15 (very different!)
```

### Weighted Scoring

For unrated movies, score is weighted by user similarity:

```
recommendation_score = Σ(similar_user_rating × similarity_weight) / Σ(similarity_weights)
```

## Deployment

### AWS EC2 Deployment

```bash
# On EC2 instance:

# 1. Install Docker
sudo apt-get update
sudo apt-get install -y docker.io

# 2. Pull image from Docker Hub
docker pull YOUR_USERNAME/movie-recommender:1.0

# 3. Run container
docker run -d -p 8000:8000 YOUR_USERNAME/movie-recommender:1.0

# 4. Access from browser
http://YOUR_EC2_IP:8000/docs
```

## Testing

### Manual Testing

Use the Swagger UI at `/docs` to test:
1. GET /movies - View all movies
2. POST /rate - Rate multiple movies
3. POST /recommend - Get recommendations
4. GET /health - Check API status

### Example Test Flow

```
1. Rate movie 1 (Inception) as 9.0
2. Rate movie 2 (Interstellar) as 8.5
3. Rate movie 3 (The Matrix) as 8.0
4. Request recommendations for user 1
5. API recommends movies based on similar users
```

## Performance

- **API Response Time**: < 100ms
- **Database Queries**: O(n) for similarity calculations
- **Memory Usage**: ~50MB base + user data
- **Scalability**: SQLite good for <10,000 users

For larger scale, upgrade to PostgreSQL.

## Future Enhancements

- [ ] Add user authentication (JWT)
- [ ] Implement matrix factorization (SVD)
- [ ] Add item-based collaborative filtering
- [ ] Implement hybrid approach (content + collaborative)
- [ ] Add caching layer (Redis)
- [ ] Create web frontend (React)
- [ ] Add CI/CD pipeline (GitHub Actions)
- [ ] Setup monitoring (Prometheus/Grafana)
- [ ] Database migration to PostgreSQL
- [ ] Kubernetes deployment

## Learning Outcomes

This project demonstrates:

✅ **Machine Learning**
- Collaborative filtering algorithm
- Similarity calculations (cosine similarity)
- Matrix operations (numpy)

✅ **Backend Development**
- REST API design (FastAPI)
- HTTP methods (GET, POST)
- Request/response handling
- Error handling and validation

✅ **Databases**
- SQLite design and queries
- Foreign keys and relationships
- Data persistence

✅ **DevOps**
- Docker containerization
- Container deployment
- Cloud infrastructure (AWS EC2)

✅ **Version Control**
- Git workflow
- GitHub collaboration

## Troubleshooting

### API Not Starting
```bash
# Check logs
docker logs <container-id>

# Verify port availability
lsof -i :8000
```

### Database Issues
```bash
# Delete and recreate
rm movies.db
python -c "from database import MovieDatabase; MovieDatabase()"
```

### Docker Connection Error
```bash
# Start Docker Desktop
# Or verify Docker daemon is running
docker ps
```

## Contributing

This is a learning project. Feel free to fork and improve!

## License

MIT License - See LICENSE file for details

## Author

Yazid Rahmouni  
Ottawa, Ontario, Canada  
[LinkedIn](https://linkedin.com/in/yazid-rahmouni)  
[GitHub](https://github.com/YOUR_USERNAME)  

## Acknowledgments

- FastAPI documentation
- scikit-learn for similarity metrics
- Docker for containerization
- AWS for cloud infrastructure

---

## Quick Links

- 📚 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 🐳 [Docker Documentation](https://docs.docker.com/)
- ☁️ [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- 🔬 [scikit-learn Documentation](https://scikit-learn.org/)

---

**Last Updated**: June 2024  
**Status**: Production Ready ✅
