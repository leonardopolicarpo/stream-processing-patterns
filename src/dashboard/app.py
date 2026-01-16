import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st

from src.dashboard.repository import DashboardRepository
from src.dashboard.views import (
  render_header,
  render_kpi_row,
  render_fraud_analysis
)

st.set_page_config(page_title="ETL Monitor", layout="wide")

def main():
  render_header()

  repo = DashboardRepository()
  metrics = repo.get_metrics()

  if metrics:
    render_kpi_row(metrics)
    st.markdown("---")
    render_fraud_analysis(metrics)
    
    st.caption(f"Última atualização do banco: {metrics.last_update}")
  else:
    st.error("Banco de dados não encontrado ou vazio. Execute o pipeline `main.py` primeiro.")

if __name__ == "__main__":
  main()