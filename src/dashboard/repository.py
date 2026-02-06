import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DashboardMetrics:
  total_tx: int
  total_volume: float
  fraud_count: int
  fraud_volume: float
  last_update: str

class DashboardRepository:
  def __init__(self):
    self.data_dir = Path(__file__).resolve().parent.parent.parent / "data"

  @st.cache_data(ttl=60, show_spinner=False)
  def get_metrics(_self, filename: str) -> DashboardMetrics | None:
    db_path = _self.data_dir / f"{filename}.db"

    if not db_path.exists():
      return None

    try:
      conn = sqlite3.connect(str(db_path))
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
        total_tx=int(row['total_tx'] or 0),
        total_volume=float(row['total_volume'] or 0.0),
        fraud_count=int(row['fraud_count'] or 0),
        fraud_volume=float(row['fraud_volume'] or 0.0),
        last_update=str(row['last_update'] or "N/A")
      )
      
    except Exception as e:
      st.error(f"Erro ao ler banco de dados: {e}")
      return None