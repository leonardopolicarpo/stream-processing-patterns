import sys
import os
import streamlit as st
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.dashboard.repository import DashboardRepository
from src.dashboard.views import (
  render_kpi_row,
  render_fraud_analysis
)

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

css_file = Path(__file__).parent.parent / "styles.css"
if css_file.exists():
  with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "shared_filename" not in st.session_state:
  st.session_state["shared_filename"] = "ledger"

current_filename = st.session_state["shared_filename"]

def main():
  st.title("📊 Financial Analytics")
  st.markdown("Visão consolidada do Ledger Financeiro.")
  st.markdown("---")

  repo = DashboardRepository()
  metrics = repo.get_metrics(current_filename)

  if metrics:
    render_kpi_row(metrics)
    st.markdown("---")
    render_fraud_analysis(metrics)
    
    st.caption(f"Última atualização do banco: {metrics.last_update}")
  else:
    st.warning("Banco de dados vazio!")
    st.info("💡 Vá até a aba **'Data Factory'** no menu lateral para gerar massa de dados.")

if __name__ == "__main__":
  main()