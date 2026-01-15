import logging
import sqlite3
from typing import List

logger = logging.getLogger(__name__)

from src.domain.transaction import Transaction
class SqliteWriter:
  def __init__(self, db_path: str):
    self.db_path = str(db_path)
    self.conn = sqlite3.connect(self.db_path)
    self._setup_db()

  def _setup_db(self):
    cursor = self.conn.cursor()

    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")

    cursor.execute("""
      CREATE TABLE IF NOT EXISTS transactions (
        id TEXT PRIMARY KEY,
        sender TEXT,
        receiver TEXT,
        amount TEXT,
        fee TEXT,
        currency TEXT,
        network TEXT,
        status TEXT,
        timestamp TEXT
      )
    """)
    self.conn.commit()
  
  def write_batch(self, batch: List[Transaction]) -> None:
    if not batch:
      return
    
    data_to_insert = [
      (
        str(t.id),
        t.sender,
        t.receiver,
        str(t.amount),
        str(t.fee),
        t.currency,
        t.network,
        t.status,
        t.timestamp.isoformat()
      )
      for t in batch
    ]

    cursor = self.conn.cursor()
    try:
      sql = """
        INSERT INTO transactions
        (id, sender, receiver, amount, fee, currency, network, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      """
      cursor.executemany(sql, data_to_insert)
    except Exception as e:
      self.conn.rollback()
      logger.error(f"Erro ao salvar batch: {e}")
      raise e
  
  def close(self):
    self.conn.close()