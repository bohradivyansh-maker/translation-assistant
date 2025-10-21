"""
Translation Memory Module
Manages SQLite database for storing translation history and ensuring consistency
"""

import logging
import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Tuple
import os

logger = logging.getLogger(__name__)


class TranslationMemory:
    """
    Manages translation memory database for consistent translations
    """
    
    def __init__(self, db_path: str = "data/translation_memory.db"):
        """
        Initialize translation memory
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connect and initialize database
        self._connect()
        self._initialize_database()
        
        logger.info(f"Translation memory initialized: {db_path}")
    
    def _connect(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def _initialize_database(self):
        """Create database tables if they don't exist"""
        try:
            cursor = self.conn.cursor()
            
            # Translations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS translations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    source_lang TEXT NOT NULL,
                    target_lang TEXT NOT NULL,
                    context TEXT,
                    domain TEXT,
                    entities TEXT,
                    confidence REAL,
                    method TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 1
                )
            """)
            
            # Create index for faster lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_translation_lookup 
                ON translations(original_text, source_lang, target_lang)
            """)
            
            # User dictionary table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_dictionary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    term TEXT NOT NULL,
                    translation TEXT NOT NULL,
                    source_lang TEXT NOT NULL,
                    target_lang TEXT NOT NULL,
                    domain TEXT,
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(term, source_lang, target_lang)
                )
            """)
            
            # Statistics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    translation_id INTEGER,
                    action TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (translation_id) REFERENCES translations(id)
                )
            """)
            
            self.conn.commit()
            logger.info("Database tables initialized")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def add_translation(
        self,
        original_text: str,
        translated_text: str,
        source_lang: str,
        target_lang: str,
        context: Optional[str] = None,
        domain: Optional[str] = None,
        entities: Optional[List[str]] = None,
        confidence: float = 1.0,
        method: str = "api"
    ) -> int:
        """
        Add a new translation to memory
        
        Args:
            original_text: Original text
            translated_text: Translated text
            source_lang: Source language code
            target_lang: Target language code
            context: Surrounding context
            domain: Domain classification
            entities: Named entities
            confidence: Translation confidence score
            method: Translation method used
            
        Returns:
            ID of inserted record
        """
        try:
            cursor = self.conn.cursor()
            
            # Check if translation already exists
            existing = self.find_translation(original_text, source_lang, target_lang)
            
            if existing:
                # Update usage count
                cursor.execute("""
                    UPDATE translations 
                    SET usage_count = usage_count + 1,
                        timestamp = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (existing['id'],))
                self.conn.commit()
                logger.info(f"Updated existing translation (ID: {existing['id']})")
                return existing['id']
            
            # Insert new translation
            entities_json = json.dumps(entities) if entities else None
            
            cursor.execute("""
                INSERT INTO translations 
                (original_text, translated_text, source_lang, target_lang, 
                 context, domain, entities, confidence, method)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                original_text, translated_text, source_lang, target_lang,
                context, domain, entities_json, confidence, method
            ))
            
            self.conn.commit()
            translation_id = cursor.lastrowid
            logger.info(f"Added new translation (ID: {translation_id})")
            return translation_id
            
        except Exception as e:
            logger.error(f"Error adding translation: {e}")
            return -1
    
    def find_translation(
        self,
        original_text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[Dict]:
        """
        Find existing translation in memory
        
        Args:
            original_text: Original text to search for
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translation dictionary or None
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                SELECT * FROM translations
                WHERE original_text = ? 
                  AND source_lang = ? 
                  AND target_lang = ?
                ORDER BY usage_count DESC, timestamp DESC
                LIMIT 1
            """, (original_text, source_lang, target_lang))
            
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
            
        except Exception as e:
            logger.error(f"Error finding translation: {e}")
            return None
    
    def search_similar_translations(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Search for similar translations (fuzzy matching)
        
        Args:
            text: Text to search for
            source_lang: Source language
            target_lang: Target language
            limit: Maximum number of results
            
        Returns:
            List of similar translations
        """
        try:
            cursor = self.conn.cursor()
            
            # Simple LIKE search (can be enhanced with FTS)
            search_pattern = f"%{text}%"
            
            cursor.execute("""
                SELECT * FROM translations
                WHERE original_text LIKE ?
                  AND source_lang = ?
                  AND target_lang = ?
                ORDER BY usage_count DESC, timestamp DESC
                LIMIT ?
            """, (search_pattern, source_lang, target_lang, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error searching translations: {e}")
            return []
    
    def add_to_user_dictionary(
        self,
        term: str,
        translation: str,
        source_lang: str,
        target_lang: str,
        domain: Optional[str] = None,
        notes: Optional[str] = None
    ) -> bool:
        """
        Add term to user dictionary
        
        Args:
            term: Original term
            translation: Translated term
            source_lang: Source language
            target_lang: Target language
            domain: Domain category
            notes: Additional notes
            
        Returns:
            True if successful
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO user_dictionary
                (term, translation, source_lang, target_lang, domain, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (term, translation, source_lang, target_lang, domain, notes))
            
            self.conn.commit()
            logger.info(f"Added to user dictionary: {term} -> {translation}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding to user dictionary: {e}")
            return False
    
    def get_user_dictionary_term(
        self,
        term: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:
        """
        Get translation from user dictionary
        
        Args:
            term: Term to look up
            source_lang: Source language
            target_lang: Target language
            
        Returns:
            Translation or None
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                SELECT translation FROM user_dictionary
                WHERE term = ? AND source_lang = ? AND target_lang = ?
            """, (term, source_lang, target_lang))
            
            row = cursor.fetchone()
            return row['translation'] if row else None
            
        except Exception as e:
            logger.error(f"Error getting user dictionary term: {e}")
            return None
    
    def get_history(
        self,
        limit: int = 50,
        source_lang: Optional[str] = None,
        target_lang: Optional[str] = None
    ) -> List[Dict]:
        """
        Get translation history
        
        Args:
            limit: Maximum number of records
            source_lang: Filter by source language
            target_lang: Filter by target language
            
        Returns:
            List of translation records
        """
        try:
            cursor = self.conn.cursor()
            
            query = "SELECT * FROM translations"
            params = []
            
            if source_lang or target_lang:
                conditions = []
                if source_lang:
                    conditions.append("source_lang = ?")
                    params.append(source_lang)
                if target_lang:
                    conditions.append("target_lang = ?")
                    params.append(target_lang)
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error getting history: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Get translation statistics
        
        Returns:
            Statistics dictionary
        """
        try:
            cursor = self.conn.cursor()
            
            stats = {}
            
            # Total translations
            cursor.execute("SELECT COUNT(*) as count FROM translations")
            stats['total_translations'] = cursor.fetchone()['count']
            
            # Total usage
            cursor.execute("SELECT SUM(usage_count) as total FROM translations")
            stats['total_usage'] = cursor.fetchone()['total'] or 0
            
            # By language pairs
            cursor.execute("""
                SELECT source_lang, target_lang, COUNT(*) as count
                FROM translations
                GROUP BY source_lang, target_lang
                ORDER BY count DESC
                LIMIT 10
            """)
            stats['top_language_pairs'] = [dict(row) for row in cursor.fetchall()]
            
            # By domain
            cursor.execute("""
                SELECT domain, COUNT(*) as count
                FROM translations
                WHERE domain IS NOT NULL
                GROUP BY domain
                ORDER BY count DESC
            """)
            stats['domain_distribution'] = [dict(row) for row in cursor.fetchall()]
            
            # User dictionary size
            cursor.execute("SELECT COUNT(*) as count FROM user_dictionary")
            stats['user_dictionary_size'] = cursor.fetchone()['count']
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
    
    def clear_history(self, days_old: Optional[int] = None):
        """
        Clear translation history
        
        Args:
            days_old: Only clear records older than this many days (None = all)
        """
        try:
            cursor = self.conn.cursor()
            
            if days_old:
                cursor.execute("""
                    DELETE FROM translations
                    WHERE timestamp < datetime('now', '-' || ? || ' days')
                """, (days_old,))
            else:
                cursor.execute("DELETE FROM translations")
            
            self.conn.commit()
            logger.info(f"Cleared history (days_old: {days_old})")
            
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Initialize memory
    memory = TranslationMemory("../data/translation_memory.db")
    
    print("=== Translation Memory Test ===\n")
    
    # Add translation
    print("Adding translation...")
    translation_id = memory.add_translation(
        original_text="Hello, world!",
        translated_text="¡Hola, mundo!",
        source_lang="en",
        target_lang="es",
        domain="casual",
        confidence=0.99
    )
    print(f"Added with ID: {translation_id}\n")
    
    # Find translation
    print("Finding translation...")
    found = memory.find_translation("Hello, world!", "en", "es")
    if found:
        print(f"Found: {found['translated_text']}")
        print(f"Usage count: {found['usage_count']}\n")
    
    # Add to user dictionary
    print("Adding to user dictionary...")
    memory.add_to_user_dictionary(
        term="algorithm",
        translation="algoritmo",
        source_lang="en",
        target_lang="es",
        domain="technical"
    )
    print("Added successfully\n")
    
    # Get statistics
    print("Statistics:")
    stats = memory.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Close connection
    memory.close()
