import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Tuple
from contextlib import contextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./qa_system.db")
DB_PATH = DATABASE_URL.replace("sqlite:///", "")

class DatabaseManager:
    """Database manager for SQLite operations"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def create_tables(self):
        """Create necessary database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create queries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    user_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    response_time REAL,
                    success BOOLEAN DEFAULT TRUE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index for better performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_queries_timestamp 
                ON queries(timestamp DESC)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_queries_user_id 
                ON queries(user_id)
            """)
            
            conn.commit()
            logger.info("Database tables created successfully")
    
    def save_query(
        self, 
        query: str, 
        response: str, 
        user_id: Optional[str] = None,
        response_time: Optional[float] = None
    ) -> int:
        """Save a query and response to the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO queries (query, response, user_id, response_time)
                VALUES (?, ?, ?, ?)
            """, (query, response, user_id, response_time))
            conn.commit()
            return cursor.lastrowid
    
    def get_query_history(
        self, 
        user_id: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[dict], int]:
        """Get query history with pagination"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Build query based on user_id
            where_clause = "WHERE user_id = ?" if user_id else ""
            params = [user_id] if user_id else []
            
            # Get total count
            count_query = f"SELECT COUNT(*) FROM queries {where_clause}"
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()[0]
            
            # Get paginated results
            query = f"""
                SELECT id, query, response, user_id, timestamp, response_time, success
                FROM queries 
                {where_clause}
                ORDER BY timestamp DESC 
                LIMIT ? OFFSET ?
            """
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Convert to dictionaries
            queries = []
            for row in rows:
                queries.append({
                    'id': row['id'],
                    'query': row['query'],
                    'response': row['response'],
                    'user_id': row['user_id'],
                    'timestamp': row['timestamp'],
                    'response_time': row['response_time'],
                    'success': bool(row['success'])
                })
            
            return queries, total_count
    
    def get_query_by_id(self, query_id: int) -> Optional[dict]:
        """Get a specific query by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, query, response, user_id, timestamp, response_time, success
                FROM queries 
                WHERE id = ?
            """, (query_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'query': row['query'],
                    'response': row['response'],
                    'user_id': row['user_id'],
                    'timestamp': row['timestamp'],
                    'response_time': row['response_time'],
                    'success': bool(row['success'])
                }
            return None

# Global database manager instance
db_manager = DatabaseManager()

def create_tables():
    """Create database tables - called during app startup"""
    db_manager.create_tables()

def save_query(query: str, response: str, user_id: Optional[str] = None, response_time: Optional[float] = None) -> int:
    """Save query to database"""
    return db_manager.save_query(query, response, user_id, response_time)

def get_query_history(user_id: Optional[str] = None, limit: int = 10, offset: int = 0) -> Tuple[List[dict], int]:
    """Get query history from database"""
    return db_manager.get_query_history(user_id, limit, offset)