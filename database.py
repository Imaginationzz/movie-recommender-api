import sqlite3
from typing import List, Dict

class MovieDatabase:
    """SQLite database for movies and user ratings"""
    
    def __init__(self, db_file="movies.db"):
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Movies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                title TEXT UNIQUE,
                year INTEGER,
                rating REAL
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE
            )
        ''')
        
        # Ratings table (user → movie ratings)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                user_id INTEGER,
                movie_id INTEGER,
                rating REAL,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(movie_id) REFERENCES movies(id),
                PRIMARY KEY(user_id, movie_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Load sample data
        self.load_sample_data()
    
    def load_sample_data(self):
        """Load sample movies"""
        movies = [
            (1, "Inception", 2010, 8.8),
            (2, "Interstellar", 2014, 8.6),
            (3, "The Matrix", 1999, 8.7),
            (4, "Dune", 2021, 8.0),
            (5, "Tenet", 2020, 7.3),
            (6, "Memento", 2000, 8.4),
            (7, "Arrival", 2016, 7.9),
            (8, "Contact", 1997, 7.4),
            (9, "2001: A Space Odyssey", 1968, 8.3),
            (10, "Dark City", 1998, 7.7),
            (11, "Blade Runner", 1982, 8.1),
            (12, "The Prestige", 2006, 8.5),
            (13, "Oppenheimer", 2023, 8.1),
            (14, "Primer", 2004, 6.8),
            (15, "Looper", 2012, 7.4),
        ]
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        for movie in movies:
            try:
                cursor.execute(
                    'INSERT INTO movies VALUES (?, ?, ?, ?)',
                    movie
                )
            except sqlite3.IntegrityError:
                pass  # Movie already exists
        
        conn.commit()
        conn.close()
    
    def add_user(self, username: str) -> int:
        """Create new user, return user ID"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        return user_id
    
    def rate_movie(self, user_id: int, movie_id: int, rating: float):
        """User rates a movie"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT OR REPLACE INTO ratings VALUES (?, ?, ?)',
            (user_id, movie_id, rating)
        )
        
        conn.commit()
        conn.close()
    
    def get_user_ratings(self, user_id: int) -> Dict[int, float]:
        """Get all ratings from a user"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT movie_id, rating FROM ratings WHERE user_id = ?',
            (user_id,)
        )
        
        ratings = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        
        return ratings
    
    def get_all_users_ratings(self) -> Dict[int, Dict[int, float]]:
        """Get all users' ratings"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id, movie_id, rating FROM ratings')
        
        all_ratings = {}
        for user_id, movie_id, rating in cursor.fetchall():
            if user_id not in all_ratings:
                all_ratings[user_id] = {}
            all_ratings[user_id][movie_id] = rating
        
        conn.close()
        
        return all_ratings
    
    def get_movie(self, movie_id: int) -> Dict:
        """Get movie details"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT id, title, year, rating FROM movies WHERE id = ?',
            (movie_id,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "title": row[1],
                "year": row[2],
                "rating": row[3]
            }
        return None
    
    def get_all_movies(self) -> List[Dict]:
        """Get all movies"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, title, year, rating FROM movies')
        
        movies = []
        for row in cursor.fetchall():
            movies.append({
                "id": row[0],
                "title": row[1],
                "year": row[2],
                "rating": row[3]
            })
        
        conn.close()
        return movies
