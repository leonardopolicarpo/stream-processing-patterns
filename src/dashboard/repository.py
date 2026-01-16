import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path
from dataclasses import dataclass

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "finance.db"

@dataclass
class DashboardMetrics:
  total_tx: int
  total_volume: float
  fraud_count: int
  fraud_volume: float
  last_update: str

class DashboardRepository:
  def __init__(self):
    self.db_path = DB_PATH

  @st.cache_data(ttl=60)
  def get_metrics(_self) -> DashboardMetrics:
    if not _self.db_path.exists():
      return None

    conn = sqlite3.connect(str(_self.db_path))
    
    query = """
    SELECT 
      COUNT(*) as total_tx,
      SUM(amount) as total_volume,
      SUM(CASE WHEN status = 'FRAUD_DETECTED' THEN 1 ELSE 0 END) as fraud_count,
      SUM(CASE WHEN status = 'FRAUD_DETECTED' THEN amount ELSE 0 END) as fraud_volume,
      MAX(timestamp) as last_update
    FROM transactions
    """
    
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
      return None

    row = df.iloc[0]
    return DashboardMetrics(
      total_tx=int(row['total_tx']),
      total_volume=float(row['total_volume']),
      fraud_count=int(row['fraud_count']),
      fraud_volume=float(row['fraud_volume']),
      last_update=str(row['last_update'])
    )