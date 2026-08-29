import sqlite3
import hashlib
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger("StorageEngine")

class StorageEngine:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS seen_events (
                    fingerprint TEXT PRIMARY KEY,
                    company_name TEXT NOT NULL,
                    source TEXT NOT NULL,
                    batch TEXT,
                    detected_at TEXT NOT NULL
                );
            """)
            conn.commit()
            logger.info("Database initialized with WAL mode enabled.")

    @staticmethod
    def generate_fingerprint(source: str, identifier: str, batch: Optional[str] = "") -> str:
        raw_key = f"{source.lower()}:{identifier.lower()}:{batch.lower() if batch else ''}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def has_seen(self, fingerprint: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM seen_events WHERE fingerprint = ?", (fingerprint,))
            return cursor.fetchone() is not None

    def record_event(self, fingerprint: str, company_name: str, source: str, batch: Optional[str]):
        now_str = datetime.utcnow().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO seen_events (fingerprint, company_name, source, batch, detected_at)
                VALUES (?, ?, ?, ?, ?)
            """, (fingerprint, company_name, source, batch, now_str))
            conn.commit()
            logger.debug(f"Recorded event fingerprint: {fingerprint}")
