import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="ETL Performance Monitor", layout="wide")

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "finance.db"

@st.cache_data(ttl=60)
def load_summary():
  if not DB_PATH.exists():
    return None
  
  conn = sqlite3.connect(str(DB_PATH))
  
  query = """
  SELECT 
    COUNT(*) as total_tx,
    SUM(CASE WHEN status = 'FRAUD_DETECTED' THEN 1 ELSE 0 END) as fraud_count,
    SUM(amount) as total_volume,
    MAX(timestamp) as last_update
  FROM transactions
  """
  df = pd.read_sql(query, conn)
  conn.close()
  return df

st.title("🚀 ETL Pipeline Dashboard")
st.markdown(f"Monitorando banco de dados em: `{DB_PATH}`")

df = load_summary()

if df is not None:
  total = df['total_tx'].iloc[0]
  frauds = df['fraud_count'].iloc[0]
  volume = df['total_volume'].iloc[0]
  
  col1, col2, col3 = st.columns(3)
  col1.metric("Total Processado", f"{total:,.0f}")
  col2.metric("Fraudes Detectadas", f"{frauds:,.0f}", delta_color="inverse")
  col3.metric("Volume Financeiro", f"R$ {volume:,.2f}")

  fraud_rate = (frauds / total) * 100 if total > 0 else 0
  st.write(f"### Taxa de Fraude: {fraud_rate:.2f}%")
  st.progress(min(fraud_rate / 100 * 5, 1.0))

else:
  st.error("Banco de dados não encontrado. Rode o ETL primeiro!")