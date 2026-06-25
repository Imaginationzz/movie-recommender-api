from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Tuple
from database import MovieDatabase

class MovieRecommender:
    """Collaborative filtering recommendation engine"""
    
    def __init__(self, db: MovieDatabase):
        self.db = db
    
    def get_recommendations(
        self, 
        user_id: int, 
        num_recommendations: int = 5
    ) -> List[Dict]:
        """
        Get movie recommendations for a user
        
        Algorithm:
        1. Find similar users (based on rating patterns)
        2. Look at movies they rated highly
        3. Suggest those movies
        """
        
        # Get all users' ratings
        all_ratings = self.db.get_all_users_ratings()
        
        if len(all_ratings) < 2:
            return self._get_popular_movies(num_recommendations)
        
        # Create rating matrix (users × movies)
        rating_matrix = self._create_rating_matrix(all_ratings)
        
        # Find similar users
        similar_users = self._find_similar_users(user_id, rating_matrix)
        
        # Get recommendations from similar users
        user_ratings = self.db.get_user_ratings(user_id)
        recommendations = self._score_recommendations(
            user_id, 
            similar_users, 
            all_ratings,
            user_ratings
        )
        
        # Return top N
        return recommendations[:num_recommendations]
    
    def _create_rating_matrix(self, all_ratings: Dict) -> Tuple:
        """
        Create matrix of user ratings
        
        Rows: Users
        Columns: Movies
        Values: Ratings (0 if not rated)
        """
        
        all_movies = self.db.get_all_movies()
        movie_ids = [m["id"] for m in all_movies]
        user_ids = sorted(all_ratings.keys())
        
        # Create matrix (users × movies)
        matrix = np.zeros((len(user_ids), len(movie_ids)))
        
        for i, user_id in enumerate(user_ids):
            for j, movie_id in enumerate(movie_ids):
                if movie_id in all_ratings[user_id]:
                    matrix[i][j] = all_ratings[user_id][movie_id]
        
        user_mapping = {uid: i for i, uid in enumerate(user_ids)}
        movie_mapping = {mid: j for j, mid in enumerate(movie_ids)}
        
        return matrix, user_mapping, movie_mapping, user_ids, movie_ids
    
    def _find_similar_users(
        self, 
        user_id: int, 
        rating_matrix: Tuple
    ) -> List[Tuple[int, float]]:
        """
        Find users with similar movie taste
        
        Uses: Cosine similarity
        Returns: List of (user_id, similarity_score)
        """
        
        matrix, user_mapping, _, user_ids, _ = rating_matrix
        
        if user_id not in user_mapping:
            return []
        
        # Get user's rating vector
        user_idx = user_mapping[user_id]
        user_vector = matrix[user_idx]
        
        # Calculate similarity with all users
        similarities = cosine_similarity([user_vector], matrix)[0]
        
        # Get similar users (excluding self)
        similar = []
        for idx, sim_score in enumerate(similarities):
            other_user_id = user_ids[idx]
            if other_user_id != user_id and sim_score > 0:
                similar.append((other_user_id, sim_score))
        
        # Sort by similarity (highest first)
        similar.sort(key=lambda x: x[1], reverse=True)
        
        return similar
    
    def _score_recommendations(
        self,
        user_id: int,
        similar_users: List[Tuple[int, float]],
        all_ratings: Dict,
        user_ratings: Dict
    ) -> List[Dict]:
        """
        Score movies based on similar users' ratings
        
        For each movie the user hasn't rated:
        - Average rating from similar users
        - Weighted by similarity score
        """
        
        scores = {}
        
        # Get all movie IDs
        all_movies = self.db.get_all_movies()
        
        for movie in all_movies:
            movie_id = movie["id"]
            
            # Skip if user already rated this
            if movie_id in user_ratings:
                continue
            
            # Calculate score from similar users
            total_score = 0
            total_weight = 0
            
            for similar_user_id, similarity in similar_users:
                if similar_user_id in all_ratings:
                    if movie_id in all_ratings[similar_user_id]:
                        # Weight rating by similarity
                        rating = all_ratings[similar_user_id][movie_id]
                        total_score += rating * similarity
                        total_weight += similarity
            
            # Average score
            if total_weight > 0:
                avg_score = total_score / total_weight
                scores[movie_id] = {
                    "score": avg_score,
                    "movie": movie
                }
        
        # Sort by score
        recommendations = []
        for movie_id in sorted(scores.keys(), 
                              key=lambda x: scores[x]["score"], 
                              reverse=True):
            rec = scores[movie_id]
            recommendations.append({
                "id": rec["movie"]["id"],
                "title": rec["movie"]["title"],
                "year": rec["movie"]["year"],
                "imdb_rating": rec["movie"]["rating"],
                "recommendation_score": round(rec["score"], 2),
                "reason": "Similar users loved this"
            })
        
        return recommendations
    
    def _get_popular_movies(self, num: int) -> List[Dict]:
        """Get most popular movies as fallback"""
        movies = self.db.get_all_movies()
        
        # Sort by IMDB rating
        movies.sort(key=lambda x: x["rating"], reverse=True)
        
        return [
            {
                "id": m["id"],
                "title": m["title"],
                "year": m["year"],
                "imdb_rating": m["rating"],
                "recommendation_score": m["rating"],
                "reason": "Popular movie"
            }
            for m in movies[:num]
        ]
