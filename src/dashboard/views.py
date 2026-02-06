import streamlit as st

from src.dashboard.repository import DashboardMetrics

def format_currency(value: float) -> str:
  if value >= 1_000_000_000:
    return f"$ {value / 1_000_000_000:.2f} B"
  elif value >= 1_000_000:
    return f"$ {value / 1_000_000:.2f} M"
  return f"$ {value:,.2f}"

def render_header():
  st.title("🚀 ETL Pipeline Analytics")
  st.markdown("Real-time transaction processing monitoring.")
  st.divider()

def render_kpi_row(metrics: DashboardMetrics):
  col1, col2, col3, col4 = st.columns(4)

  col1.metric("Total Processed", f"{metrics.total_tx:,.0f}")
  
  col2.metric("Total Volume", format_currency(metrics.total_volume))
  
  col3.metric(
    "Blocked Frauds", 
    f"{metrics.fraud_count:,.0f}",
    delta_color="inverse"
  )
  
  col4.metric(
    "Loss Prevented", 
    format_currency(metrics.fraud_volume),
    delta_color="normal"
  )

def render_fraud_analysis(metrics: DashboardMetrics):
  if metrics.total_tx == 0:
    return

  fraud_rate = (metrics.fraud_count / metrics.total_tx) * 100
  
  st.subheader("🛡️ Security Analysis")
  st.write(f"**Fraud Attempt Rate:** {fraud_rate:.2f}%")
  
  st.progress(min(fraud_rate / 100, 1.0))
  
  if fraud_rate > 15:
    st.warning(f"⚠️ Alert: Abnormally high fraud rate ({fraud_rate:.2f}%) detected.")